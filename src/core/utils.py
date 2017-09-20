from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.constructors import bits


class UserKeyConstructor(DefaultKeyConstructor):
    user = bits.UserKeyBit()
