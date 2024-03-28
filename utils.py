import os
import random
import smtplib
import collections
import collections.abc
import sys
from datetime import date, datetime

from accounts.models import CustomUser
from billing.models import paymentProfile

collections.MutableSequence = collections.abc.MutableSequence
from django.core.mail import send_mail
from django.template.loader import render_to_string

from emails.models import EmailRecords

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import Decimal


import logging
import pyxb

# Set the logging level to DEBUG for PyXB module
logging.getLogger('pyxb').setLevel(logging.DEBUG)

merchantAuth = apicontractsv1.merchantAuthenticationType()
merchantAuth.name = os.environ.get('AUTHNET_NAME')
merchantAuth.transactionKey = os.environ.get('AUTHNET_TRANSACTION_KEY')


# Now you can use MutableSequence


def send_custom_email(rec_email, subject, template_name, context, rec_id):
    print('attempting email send')
    print(rec_email)
    email_content = render_to_string(f'email_templates/{template_name}', context)

    try:
        sent_email = send_mail(
            subject=subject,
            message='',
            html_message=email_content,
            from_email='rdevcotest@gmail.com',
            recipient_list=[rec_email]
        )
        print(sent_email)
        email_record = EmailRecords(user_id=rec_id, subject=subject, content=email_content)
        email_record.save()
        return 'worked'
    except smtplib.SMTPException as e:
        print(e)
        return 'didnt work'


def charge_cc(amount, form=None):
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = form["card_number"]
    creditCard.expirationDate = form["expiration_date"]
    creditCard.cardCode = form["cvc"]

    billTo = apicontractsv1.customerAddressType()
    billTo.firstName = form["first_name"]
    billTo.lastName = form["last_name"]
    billTo.address = form["address"]
    billTo.city = form["city"]
    billTo.state = form["state"]
    billTo.zip = form["zip"]


    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = payment
    transactionrequest.billTo = billTo

    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    # createtransactionrequest.refId = "MerchantID-0001"

    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()
    print(response)

    if (response.messages.resultCode == "Ok"):
        print("Transaction ID : %s" % response.transactionResponse.transId)
        return response.messages.resultCode
    else:
        print("response code: %s" % response.messages.resultCode)
        return None


def create_customer_profile(user_id=None, form=None):
    print("hello2")
    user = CustomUser.objects.get(id=user_id)
    print(user.authnet_id)
    if not user.authnet_id:
        print("hello3")
        createCustomerProfile = apicontractsv1.createCustomerProfileRequest()
        createCustomerProfile.merchantAuthentication = merchantAuth
        createCustomerProfile.profile = apicontractsv1.customerProfileType(user.ship_fname+user.ship_lname, user.email_address)

        controller = createCustomerProfileController(createCustomerProfile)
        controller.execute()

        response = controller.getresponse()
        user.authnet_id = str(response.customerProfileId)
        user.save()

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = form["card_number"]
        creditCard.expirationDate = form["expiration_date"]
        creditCard.cardCode = form["cvc"]

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        billTo = apicontractsv1.customerAddressType()
        billTo.firstName = form["first_name"]
        billTo.lastName = form["last_name"]
        billTo.address = form["address"]
        billTo.city = form["city"]
        billTo.state = form["state"]
        billTo.zip = form["zip"]
        billTo.country = form["country"]

        profile = apicontractsv1.customerPaymentProfileType()
        profile.payment = payment
        profile.billTo = billTo

        createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
        createCustomerPaymentProfile.merchantAuthentication = merchantAuth
        createCustomerPaymentProfile.paymentProfile = profile
        print("customerProfileId in create_customer_payment_profile. customerProfileId = %s" % response.customerProfileId)
        createCustomerPaymentProfile.customerProfileId = str(response.customerProfileId)

        payment_controller = createCustomerPaymentProfileController(createCustomerPaymentProfile)
        payment_controller.execute()

        payment_response = payment_controller.getresponse()

        new_payment_profile = paymentProfile(user_id=user, profile_number=payment_response.customerPaymentProfileId)
        new_payment_profile.save()

        if (response.messages.resultCode == "Ok"):
            print("Successfully created a customer profile with id: %s" % response.customerProfileId)
        else:
            print("Failed to create customer payment profile %s" % response.messages.message[0]['text'].text)
        print("tryingg")
        print(payment_response.customerPaymentProfileId)
        print("again")
        print(response.customerProfileId)
        return {"payment_profile": payment_response.customerPaymentProfileId, "customer_profile": response.customerProfileId}


# if (os.path.basename(__file__) == os.path.basename(sys.argv[0])):
#     create_customer_profile()


# if (os.path.basename(__file__) == os.path.basename(sys.argv[0])):
#     create_customer_payment_profile(constants.customerProfileId)


def charge_existing_customer(customer_profile, payment_profile, amount):
    profileToCharge = apicontractsv1.customerProfilePaymentType()
    profileToCharge.customerProfileId = customer_profile
    profileToCharge.paymentProfile = apicontractsv1.paymentProfile()
    profileToCharge.paymentProfile.paymentProfileId = payment_profile

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.profile = profileToCharge

    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth

    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    print("response.messages.resultCode")
    print(response.messages.resultCode)
    if response.messages.resultCode == "Ok":
        return response
    else:
        return None


def get_payment_profiles(customer_profile, payment_profile):
    getCustomerPaymentProfile = apicontractsv1.getCustomerPaymentProfileRequest()
    getCustomerPaymentProfile.merchantAuthentication = merchantAuth
    getCustomerPaymentProfile.customerProfileId = customer_profile
    getCustomerPaymentProfile.customerPaymentProfileId = payment_profile
    getCustomerPaymentProfile.unmaskExpirationDate = True

    controller = getCustomerPaymentProfileController(getCustomerPaymentProfile)
    controller.execute()
    response = controller.getresponse()
    print(response)

    profile = {
        'card_num': response.paymentProfile.payment.creditCard.cardNumber,
        'expiration': response.paymentProfile.payment.creditCard.expirationDate,
        'billing_address': response.paymentProfile.billTo.address,
        'billing_city': response.paymentProfile.billTo.city,
        'billing_state': response.paymentProfile.billTo.state,
        'billing_zip': response.paymentProfile.billTo.zip,
        'billing_firstName': response.paymentProfile.billTo.firstName,
        'billing_lastName': response.paymentProfile.billTo.lastName,
        'payment_profile': payment_profile
    }

    return profile


def delete_pay(customer_profile, payment_profile):
    deleteCustomerPaymentProfile = apicontractsv1.deleteCustomerPaymentProfileRequest()
    deleteCustomerPaymentProfile.merchantAuthentication = merchantAuth
    deleteCustomerPaymentProfile.customerProfileId = customer_profile
    deleteCustomerPaymentProfile.customerPaymentProfileId = payment_profile

    controller = deleteCustomerPaymentProfileController(deleteCustomerPaymentProfile)
    controller.execute()

    response = controller.getresponse()

    if (response.messages.resultCode == "Ok"):
        print("Successfully deleted customer payment profile with customer profile id %s" % deleteCustomerPaymentProfile.customerProfileId)

        return 1

def add_pay(customer_profile, form=None):
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = form["card_number"]
    creditCard.expirationDate = form['expiration_date']
    creditCard.cardCode = form['cvc']

    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    billTo = apicontractsv1.customerAddressType()
    billTo.firstName = form['first_name']
    billTo.lastName = form['last_name']
    billTo.address = form['address']
    billTo.city = form['city']
    billTo.state = form['state']
    billTo.zip = form['zip']

    profile = apicontractsv1.customerPaymentProfileType()
    profile.payment = payment
    profile.billTo = billTo

    createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
    createCustomerPaymentProfile.merchantAuthentication = merchantAuth
    createCustomerPaymentProfile.paymentProfile = profile
    print("customerProfileId in create_customer_payment_profile. customerProfileId = %s" % customer_profile)
    createCustomerPaymentProfile.customerProfileId = str(customer_profile)

    controller = createCustomerPaymentProfileController(createCustomerPaymentProfile)
    controller.execute()

    response = controller.getresponse()
    print('Error Code: %s' % response.messages.message[0]['code'].text)
    print('Error message: %s' % response.messages.message[0]['text'].text)
    print(response.messages.resultCode)
    print(response.customerPaymentProfileId)

    if (response.messages.resultCode == "Ok"):
        print("Successfully created a customer payment profile with id: %s" % response.customerPaymentProfileId)
        user = CustomUser.objects.get(authnet_id=customer_profile)
        pay_profile = paymentProfile(user_id=user, profile_number=response.customerPaymentProfileId)
        pay_profile.save()
        return response.customerPaymentProfileId
    else:
        return None

def recurring_pay(amount, form=None):
    y = datetime.now().year
    m = datetime.now().month
    d = datetime.now().day
    print(f"{y}, {d}, {m}")
    # Setting payment schedule
    paymentschedule = apicontractsv1.paymentScheduleType()
    paymentschedule.interval = apicontractsv1.paymentScheduleTypeInterval()  # apicontractsv1.CTD_ANON() #modified by krgupta
    paymentschedule.interval.length = 1
    paymentschedule.interval.unit = apicontractsv1.ARBSubscriptionUnitEnum.months
    paymentschedule.startDate = datetime(y, m, d)
    paymentschedule.totalOccurrences = 9999
    # paymentschedule.trialOccurrences = 1
    # Giving the credit card info
    creditcard = apicontractsv1.creditCardType()
    creditcard.cardNumber = form['card_number']
    creditcard.expirationDate = form['expiration_date']
    payment = apicontractsv1.paymentType()
    payment.creditCard = creditcard
    # Setting billing information
    billto = apicontractsv1.nameAndAddressType()
    billto.firstName = form['first_name']
    billto.lastName = form['last_name']
    billto.address = form['address']
    billto.city = form['city']
    billto.state = form['state']
    billto.zip = form['zip']
    # Setting subscription details
    subscription = apicontractsv1.ARBSubscriptionType()
    subscription.name = "Sample Subscription"
    subscription.paymentSchedule = paymentschedule
    subscription.amount = amount
    subscription.trialAmount = Decimal('0.00')
    subscription.billTo = billto
    subscription.payment = payment
    # Creating the request
    request = apicontractsv1.ARBCreateSubscriptionRequest()
    request.merchantAuthentication = merchantAuth
    request.subscription = subscription
    # Creating and executing the controller
    controller = ARBCreateSubscriptionController(request)
    controller.execute()
    # Getting the response
    response = controller.getresponse()
    user = CustomUser.objects.get(authnet_id=response.profile.customerProfileId)
    pay_profile = paymentProfile(user_id=user, profile_number=response.profile.customerPaymentProfileId)

    return response.profile.customerPaymentProfileId
