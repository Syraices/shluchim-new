import os
import random
import smtplib
import collections
import collections.abc
import sys
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
merchantAuth.name = '6QLmSgk4T65y'
merchantAuth.transactionKey = '9LYsRz39455m49Ha'


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


def charge_cc():
    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = "4111111111111111"
    creditCard.expirationDate = "2024-12"

    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authOnlyTransaction"
    transactionrequest.amount = Decimal('1.65')
    transactionrequest.payment = payment

    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "MerchantID-0001"

    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if (response.messages.resultCode == "Ok"):
        print("Transaction ID : %s" % response.transactionResponse.transId)
    else:
        print("response code: %s" % response.messages.resultCode)


def create_customer_profile(user_id=1):
    print("hello2")
    user = CustomUser.objects.get(id=user_id)
    print(user.authnet_id)
    if not user.authnet_id:
        print("hello3")
        createCustomerProfile = apicontractsv1.createCustomerProfileRequest()
        createCustomerProfile.merchantAuthentication = merchantAuth
        createCustomerProfile.profile = apicontractsv1.customerProfileType('jdoe' + str(random.randint(0, 10000)),
                                                                           'John23Doe', 'jdoe@mail.com')

        controller = createCustomerProfileController(createCustomerProfile)
        controller.execute()

        response = controller.getresponse()
        user.authnet_id = str(response.customerProfileId)
        user.save()

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = "4111111111111111"
        creditCard.expirationDate = "2035-12"
        creditCard.cardCode = "123"

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        billTo = apicontractsv1.customerAddressType()
        billTo.firstName = "John"
        billTo.lastName = "Snow"
        billTo.address = "3534 Arcadia St"
        billTo.city = "Skokie"
        billTo.state = "IL"
        billTo.zip = "60203"
        billTo.country = "USA"

        profile = apicontractsv1.customerPaymentProfileType()
        profile.payment = payment
        profile.billTo = billTo

        createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
        createCustomerPaymentProfile.merchantAuthentication = merchantAuth
        createCustomerPaymentProfile.paymentProfile = profile
        print(
            "customerProfileId in create_customer_payment_profile. customerProfileId = %s" % response.customerProfileId)
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

        return response


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

    print("hello")


def get_payment_profiles(customer_profile, payment_profile):
    getCustomerPaymentProfile = apicontractsv1.getCustomerPaymentProfileRequest()
    getCustomerPaymentProfile.merchantAuthentication = merchantAuth
    getCustomerPaymentProfile.customerProfileId = customer_profile
    getCustomerPaymentProfile.customerPaymentProfileId = payment_profile
    getCustomerPaymentProfile.unmaskExpirationDate = True

    controller = getCustomerPaymentProfileController(getCustomerPaymentProfile)
    controller.execute()
    response = controller.getresponse()

    profile = {
        'card_num': response.paymentProfile.payment.creditCard.cardNumber,
        'expiration': response.paymentProfile.payment.creditCard.expirationDate,
        'billing_address': response.paymentProfile.billTo.address,
        'billing_city': response.paymentProfile.billTo.city,
        'billing_state': response.paymentProfile.billTo.state,
        'billing_zip': response.paymentProfile.billTo.zip,
        'billing_firstName': response.paymentProfile.billTo.firstName,
        'billing_lastName': response.paymentProfile.billTo.lastName,
    }

    return profile
