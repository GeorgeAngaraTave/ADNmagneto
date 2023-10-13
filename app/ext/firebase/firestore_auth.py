# -*- coding: utf-8 -*-

"""Python module for Firebase Auth."""

import firebase_admin
from firebase_admin import auth
from app.ext.utils import Commons

class FirebaseAuth:

    @staticmethod
    def get_list_users():
        """Start listing users from the beginning, 1000 at a time."""

        page_list_user = auth.list_users()
        users_list = []

        # Iterate through all users. This will still retrieve users in batches,
        # buffering no more than 1000 users in memory at a time.

        for user in page_list_user.iterate_all():
            if hasattr(user, '_data'):
                users_list.append({"UserID": user.uid, "data": user._data})
            else:
                users_list.append({"UserID": user.uid, "data": user.__dict__})

        return users_list

    @staticmethod
    def create_user(user_data):
        if user_data is None:
            reason = 'FirebaseAuth create_user Exception: data is missing'
            print(reason)
            return reason

        if 'email' not in user_data:
            reason = 'FirebaseAuth create_user Exception: email is missing'
            print(reason)
            return reason

        if 'password' not in user_data:
            reason = 'FirebaseAuth create_user Exception: password is missing'
            print(reason)
            return reason

        try:
            user = auth.create_user(
                email=user_data['email'],
                email_verified=user_data['email_verified'] if 'email_verified' in user_data else False,
                phone_number=user_data['phone_number'] if 'phone_number' in user_data else None,
                password=user_data['password'],
                display_name=user_data['display_name'] if 'display_name' in user_data else None,
                photo_url=user_data['photo_url'] if 'photo_url' in user_data else None,
                disabled=user_data['disabled'] if 'disabled' in user_data else False,
            )

            if user is not None:
                print('FirebaseAuth create_user:', user.uid)
                return user.uid

            return None
        except Exception as e:
            print('FirebaseAuth create_user Exception:', e)
            return e

    @staticmethod
    def create_user_with_phone(user_data):
        if user_data is None:
            reason = 'FirebaseAuth create_user_with_phone Exception: data is missing'
            print(reason)
            return reason

        if 'phone_number' not in user_data:
            reason = 'FirebaseAuth create_user_with_phone Exception: phone_number is missing'
            print(reason)
            return reason

        if 'password' not in user_data:
            reason = 'FirebaseAuth create_user_with_phone Exception: password is missing'
            print(reason)
            return reason

        try:
            user = auth.create_user(
                phone_number=user_data['phone_number'],
                password=user_data['password'],
                display_name=user_data['display_name'] if 'display_name' in user_data else None,
                photo_url=user_data['photo_url'] if 'photo_url' in user_data else None,
                disabled=user_data['disabled'] if 'disabled' in user_data else False,
            )

            print('FirebaseAuth create_user_with_phone:', user.uid)
            if user is not None:
                return user.uid

            return None
        except Exception as e:
            print('FirebaseAuth create_user_with_phone Exception:', e)
            return e

    @staticmethod
    def get_user_by_uuid(uid, to_json=False):
        if uid is None:
            print('FirebaseAuth get_user_by_uuid Exception: uid is missing')
            return None

        try:
            user = auth.get_user(uid)

            if to_json is True:
                if isinstance(user, firebase_admin._user_mgt.UserRecord):
                    if hasattr(user, '_data'):
                        return user._data
                    else:
                        return user.__dict__
            else:
                return user
        except Exception as e:
            print('FirebaseAuth get_user_by_uuid Exception:', e)
            return None

    @staticmethod
    def get_user_by_email(email, to_json):
        if email is None:
            reason = 'FirebaseAuth get_user_by_email Exception: email is missing'
            print(reason)
            return reason

        try:
            user = auth.get_user_by_email(email)
            if to_json is True:
                if isinstance(user, firebase_admin._user_mgt.UserRecord):
                    return user.__dict__
            else:
                return user
        except Exception as e:
            print('FirebaseAuth get_user_by_email Exception:', e)
            return e

    @staticmethod
    def get_user_by_phone_number(phone):
        if phone is None:
            reason = 'FirebaseAuth get_user_by_phone_number Exception: phone is missing'
            print(reason)
            raise Exception(reason)

        try:
            user = auth.get_user_by_phone_number(phone)

            return user
        except Exception as e:
            print('FirebaseAuth get_user_by_phone_number Exception:', e)
            raise Exception(e)

    @staticmethod
    def update_user(uid, user_data):
        if uid is None:
            reason = 'FirebaseAuth update_user Exception: uid is missing'
            print(reason)
            return reason

        if user_data is None:
            reason = 'FirebaseAuth update_user Exception: data is missing'
            print(reason)
            return reason

        if 'email' not in user_data:
            reason = 'FirebaseAuth update_user Exception: email is missing'
            print(reason)
            return reason

        if 'password' not in user_data:
            reason = 'FirebaseAuth update_user Exception: password is missing'
            print(reason)
            return reason

        try:
            result = auth.update_user(
                uid,
                email=user_data['email'],
                phone_number=user_data['phone_number'] if 'phone_number' in user_data else None,
                email_verified=user_data['email_verified'] if 'email_verified' in user_data else True,
                password=user_data['password'],
                display_name=user_data['display_name'] if 'display_name' in user_data else None,
                photo_url=user_data['photo_url'] if 'photo_url' in user_data else None,
                disabled=user_data['disabled'] if 'disabled' in user_data else False,
            )

            # return None
            if result is not None:
                print("FirebaseAuth update_user:", result.uid)
                return result.uid

            return None
        except Exception as e:
            print('FirebaseAuth update_user Exception:', e)
            return e

    @staticmethod
    def delete_user(uid):
        if uid is None:
            reason = 'FirebaseAuth delete_user Exception: password is missing'
            print(reason)
            return reason

        try:
            auth.delete_user(uid)

            return None
        except Exception as e:
            print('FirebaseAuth delete_user Exception:', e)
            return e

    @staticmethod
    def delete_massive_users(user_uid_list):
        if user_uid_list is None:
            reason = 'FirebaseAuth delete_massive_users Exception: user_uid_list is missing'
            print(reason)
            return reason

        if not Commons.is_iterable(user_uid_list):
            reason = 'FirebaseAuth delete_massive_users Exception: user_uid_list must be iterable'
            print(reason)
            return reason

        try:
            if not hasattr(auth, 'delete_users'):
                print("FirebaseAuth delete_massive_users Exception: auth has no attribute delete_users")
                reason = 'Please update Firebase Auth and retry again'
                print(reason)
                # return reason

                for item in user_uid_list:
                    auth.delete_user(item)
                    print("Successfully deleted {0} user ID".format(item))

                return None

            result = auth.delete_users(user_uid_list)

            print('FirebaseAuth delete_massive_users: Successfully deleted {0} users'.format(result.success_count))
            print('FirebaseAuth delete_massive_users: Failed to delete {0} users'.format(result.failure_count))

            for err in result.errors:
                print('error #{0}, reason: {1}'.format(result.index, result.reason))

            if err is not None:
                return err

            return None
        except Exception as e:
            print('FirebaseAuth delete_massive_users Exception:', e)
            return e

    @staticmethod
    def disable_user(uid):
        if uid is None:
            reason = 'FirebaseAuth disable_user Exception: uid is missing'
            print(reason)
            return reason

        try:
            result = auth.update_user(uid, disabled=True)

            if result is not None:
                print("FirebaseAuth disable_user:", result.uid)
                return result.uid

            return None
        except Exception as e:
            print('FirebaseAuth disable_user Exception:', e)
            return e

    @staticmethod
    def enable_user(uid):
        if uid is None:
            reason = 'FirebaseAuth enable_user Exception: uid is missing'
            print(reason)
            return reason

        try:
            result = auth.update_user(uid, disabled=False)

            if result is not None:
                print("FirebaseAuth enable_user:", result.uid)
                return result.uid

            return None
        except Exception as e:
            print('FirebaseAuth enable_user Exception:', e)
            return e

    @staticmethod
    def reset_password( email ):
        try:
            action_code_settings = auth.ActionCodeSettings(
                url = 'magneto-dot-invertible-eye-316323.uc.r.firebaseapp.com/checkout?cartId=1234' # TODO validar enlace de retorno
            )

            link = auth.generate_password_reset_link( email, action_code_settings )

            return link

        except Exception as e:
            print('FirebaseAuth reset_password Exception: ', e)
            raise Exception(e)
