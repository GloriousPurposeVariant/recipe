from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser, Profile
from recipe.models import Recipe, RecipeCategory
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )
        self.client.force_authenticate(user=self.user)
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.profile, created = Profile.objects.get_or_create(user=self.user, defaults={'bio': "This is a bio"})
        self.category = RecipeCategory.objects.create(name="Test Category")
        self.recipe = Recipe.objects.create(
            title="Test Recipe 1",
            author=self.user,
            category=self.category,
            cook_time="00:30:00",
            ingredients="Test ingredients",
            procedure="Test procedure",
        )

        

    def test_get_user_info(self):
        response = self.client.get(reverse('users:user-info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_user_info(self):
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com'
        }
        response = self.client.put(reverse('users:user-info'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
        self.assertEqual(response.data['email'], 'updateduser@example.com')

    def test_partial_update_user_info(self):
        data = {
            'username': 'partiallyupdateduser'
        }
        response = self.client.patch(reverse('users:user-info'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'partiallyupdateduser')

    def test_update_user_info_invalid(self):
        data = {
            'username': '',
            'email': 'invalid_email'
        }
        response = self.client.put(reverse('users:user-info'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_info_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('users:user-info'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(reverse('users:login-user'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        
    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(reverse('users:create-user'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        
    def test_user_login_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('users:login-user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Incorrect Credentials')
        
    def test_user_login_nonexistent_user(self):
        data = {
            'email': 'nonexistentuser',
            'password': 'password123'
        }
        response = self.client.post(reverse('users:login-user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    def test_user_logout(self):
        self.client.force_authenticate(user=self.user)  # Ensure the user is authenticated
        data = {
            'refresh': self.refresh_token
        }
        response = self.client.post(reverse('users:logout-user'), data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        
    def test_user_logout_invalid_token(self):
        self.client.force_authenticate(user=self.user)  # Ensure the user is authenticated
        data = {
            'refresh': 'invalidtoken'
        }
        response = self.client.post(reverse('users:logout-user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout_unauthenticated(self):
        self.client.logout()  # Ensure the user is logged out
        data = {
            'refresh': self.refresh_token
        }
        response = self.client.post(reverse('users:logout-user'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_password_change_valid(self):
        data = {
            'old_password': 'password123',
            'new_password': 'newpassword123'
        }
        response = self.client.put(reverse('users:change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({}, response.json())
        
    def test_password_change_invalid_old_password(self):
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123'
        }
        response = self.client.put(reverse('users:change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_change_unauthenticated(self):
        self.client.logout()
        data = {
            'old_password': 'password123',
            'new_password': 'newpassword123'
        }
        response = self.client.put(reverse('users:change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_password_reset(self):
        data = {
            'email': 'testuser@example.com'
        }
        response = self.client.post(reverse('password_reset:reset-password-request'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'OK')
        

    def test_password_change_invalid_old_password(self):
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123'
        }
        response = self.client.put(reverse('users:change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_unauthenticated(self):
        self.client.logout()
        data = {
            'old_password': 'password123',
            'new_password': 'newpassword123'
        }
        response = self.client.put(reverse('users:change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_user_profile(self):
        response = self.client.get(reverse('users:user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], self.profile.bio)
        
    def test_update_user_profile(self):
        
        data = {
            'bio': 'Updated bio',
            'bookmarks': [self.recipe.id]  # Include a valid bookmark or keep it empty
        }
        response = self.client.put(reverse('users:user-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')
        self.assertIn(self.recipe, self.user.profile.bookmarks.all())
        
    def test_patch_user_profile(self):
        data = {
            'bio': 'Updated bio'
        }
        response = self.client.patch(reverse('users:user-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')


    def test_patch_user_profile_unauthenticated(self):
        self.client.logout()
        data = {
            'bio': 'Updated bio'
        }
        response = self.client.patch(reverse('users:user-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    
    def test_get_user_bookmarks(self):
        # Ensure there are no bookmarks initially
        response = self.client.get(reverse('users:user-bookmark', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
    def test_post_user_bookmark(self):
        data = {
            'id': self.recipe.id  # Assuming the recipe ID is required
        }
        response = self.client.post(reverse('users:user-bookmark', kwargs={'pk': self.user.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the recipe was added to bookmarks
        self.profile.refresh_from_db()
        self.assertIn(self.recipe, self.profile.bookmarks.all())
    
    def test_post_user_bookmark(self):
        data = {
            'id': self.recipe.id  # Assuming the recipe ID is required
        }
        response = self.client.post(reverse('users:user-bookmark', kwargs={'pk': self.user.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the recipe was added to bookmarks
        self.profile.refresh_from_db()
        self.assertIn(self.recipe, self.profile.bookmarks.all())
        
    def test_delete_user_bookmark(self):
        # First, add a bookmark
        self.profile.bookmarks.add(self.recipe)

        data = {
            'id': self.recipe.id  # Assuming the recipe ID is required
        }
        response = self.client.delete(reverse('users:user-bookmark', kwargs={'pk': self.user.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the recipe was removed from bookmarks
        self.profile.refresh_from_db()
        self.assertNotIn(self.recipe, self.profile.bookmarks.all())

    def test_get_user_bookmarks_unauthenticated(self):
        self.client.logout()  # Ensure the user is logged out
        response = self.client.get(reverse('users:user-bookmark', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_post_user_bookmark_unauthenticated(self):
        self.client.logout()  # Ensure the user is logged out
        data = {
            'id': self.recipe.id
        }
        response = self.client.post(reverse('users:user-bookmark', kwargs={'pk': self.user.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_bookmark_unauthenticated(self):
        self.client.logout()  # Ensure the user is logged out
        data = {
            'id': self.recipe.id
        }
        response = self.client.delete(reverse('users:user-bookmark', kwargs={'pk': self.user.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_avatar_authenticated(self):
        response = self.client.get(reverse('users:user-avatar'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('avatar', response.data)

    def test_custom_user_str(self):
        self.assertEqual(str(self.user), 'testuser@example.com')
        
    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser')
        
    
    


        
   
