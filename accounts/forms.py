from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import InlineField, FormActions, InlineCheckboxes

from django.contrib.auth import get_user_model
from plans.models import Plan
from .models import CustomUser

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
    class Meta:
        model = CustomUser
        fields = (
            'ship_address',
            'ship_city',
            'ship_state',
            'ship_zip',
        )


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'phone_number',
            'four_pin',
            'ship_fname',
            'ship_lname',
            'ship_address',
            'ship_city',
            'ship_state',
            'ship_zip',
            'is_billing'
        )
        widgets = {
            'is_billing': forms.CheckboxInput,
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'four_pin': 'Four Digit Pin',
            'ship_fname': 'Fisrt Name',
            'ship_lname': 'Last Name',
            'ship_address': 'Address',
            'ship_city': 'City',
            'ship_state': 'State',
            'ship_zip': 'Zipcode',
            'is_billing': 'Billing is same as shipping'
        }




class CustomUserPlanChange(UserChangeForm):
    plan_list = Plan.objects.all()

    # plan_id_box = forms.MultipleChoiceField(
    #     required=True,
    #     widget=forms.CheckboxSelectMultiple(attrs={'template': 'templates/checkbox.html'}),
    #     choices=(
    #         # (plan_list[0].name, plan_list[0].name),
    #         # (plan_list[1].name, plan_list[1].name)
    #     )
    #
    # )

    # plan_id_label = forms.CharField(label='Plan')
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        # fields = ('plan_id_box',)
        # labels = {
        #     'plan_id_box': 'Plan'
        # }
        exclude = ("password",)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # current_plan = self.request.user.plan_id
            print("ftft")
            # print(current_plan)
            print('current_plan')
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))

            self.helper.layout = Layout(

                # InlineCheckboxes('plan_id', ),
                FormActions(
                    Submit('submit', 'Submit')
                )
            )
