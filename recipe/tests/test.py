from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from recipe.models import (
    Recipe,
    RecipeCategory,
    RecipeLike,
    get_default_recipe_category,
)
import base64
from io import BytesIO
from PIL import Image
from recipe.serializers import RecipeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class RecipeAPITestCase(APITestCase):

    def setUp(self):
        # Create test data
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        self.other_user = CustomUser.objects.create_user(
            username="otheruser",
            password="otherpassword",
            email="otheruser@example.com",
        )
        self.category = RecipeCategory.objects.create(name="Test Category")

        self.recipe1 = Recipe.objects.create(
            title="Test Recipe 1",
            author=self.user,
            category=self.category,
            cook_time="00:30:00",
            ingredients="Test ingredients",
            procedure="Test procedure",
        )

        self.recipe_like = RecipeLike.objects.create(
            user=self.user, recipe=self.recipe1
        )
        self.detail_url = reverse(
            "recipe:recipe-detail", kwargs={"pk": self.recipe1.id}
        )
        self.create_url = reverse("recipe:recipe-create")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.like_url = reverse("recipe:recipe-like", kwargs={"pk": self.recipe1.id})

        

    def get_temporary_image_file(self):
    # Create a temporary image in memory
        img = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)

        # Create a SimpleUploadedFile for the image
        return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")
    
#     def test_create_recipe(self): # Todo: Conflict multipart nested object?
#         temp_image = self.get_temporary_image_file()
#     #     # Recipe data
#         data = {
#             "title": "New Test Recipe",
#             "category": {},
#             "desc": "New description",
#             "cook_time": "01:00:00",
#             "ingredients": "New ingredients",
#             "procedure": "New procedure",
#             "picture": temp_image
#         }
# # 
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

#         # # POST request to create the recipe
#         response = self.client.post(self.create_url, data=data, format="multipart")
#         print(response.json(), "print the response data for debugging")
#         print(response.data)

#         # Assert the response status code
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Check if the recipe was created and the author was assigned correctly
#         recipe = Recipe.objects.get(title="New Test Recipe")
#         self.assertEqual(recipe.author, self.user)
#         self.assertEqual(recipe.desc, data["desc"])
#         self.assertEqual(recipe.cook_time, data["cook_time"])
#         self.assertEqual(recipe.ingredients, data["ingredients"])
#         self.assertEqual(recipe.procedure, data["procedure"])
#         self.assertEqual(recipe.category.name, data["category"]["name"])

        # Optionally, print the response data for debugging

    def test_get_recipe_detail(self):
        # self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # GET request to retrieve the recipe details
        response = self.client.get(self.detail_url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the response data structure and content
        expected_data = RecipeSerializer(self.recipe1).data
        self.assertEqual(response.data, expected_data)

    # def test_update_recipe(self): # Todo: Conflict multipart nested object?
    #     self.client.force_authenticate(user=self.user)
    #     print(self.category, 'aaaaaaaaaa')
    #     updated_data = {
    #         "title": "Updated Recipe Title",
    #         "category": {'name': "new category"},
    #         "desc": "Updated description",
    #         "cook_time": "01:00:00",
    #         "ingredients": "Updated ingredients",
    #         "procedure": "Updated procedure",
    #     }
    #     response = self.client.put(self.detail_url, updated_data, format="json")
    #     print(response.json())

    #     # Assert the response status code
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Validate the updated data
    #     self.recipe.refresh_from_db()
    #     self.assertEqual(self.recipe1.title, updated_data["title"])
    #     self.assertEqual(self.recipe1.cook_time, updated_data["cook_time"])
    #     self.assertEqual(self.recipe1.ingredients, updated_data["ingredients"])
    #     self.assertEqual(self.recipe1.procedure, updated_data["procedure"])
        
    def test_partial_update_recipe(self):
        self.client.force_authenticate(user=self.user)

        # Data for partial update
        updated_data = {
            "title": "Partially Updated Recipe Title",
            "desc": "Partially updated description",
        }

        # PATCH request to partially update the recipe
        response = self.client.patch(self.detail_url, data=updated_data, format="json")

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the recipe instance from the database
        self.recipe1.refresh_from_db()

        # Validate that the title and description were updated
        self.assertEqual(self.recipe1.title, updated_data["title"])
        self.assertEqual(self.recipe1.desc, updated_data["desc"])

        # Check that other fields remain unchanged
        expected_cook_time = datetime.time(0, 30) 
        self.assertEqual(self.recipe1.cook_time, expected_cook_time)

    def test_get_recipe_list(self):
        url = reverse("recipe:recipe-list")
        # Simulate a GET request to /api/recipe/
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the response data structure and content
        expected_data = RecipeSerializer(
            instance=[self.recipe1], many=True
        ).data  
        self.assertEqual(response.data, expected_data)

        for recipe_data in response.data:
            self.assertIn("title", recipe_data)
            self.assertEqual(recipe_data["title"], self.recipe1.title)

    def test_recipe_category_str(self):
        """Test the string representation of RecipeCategory"""
        category = RecipeCategory.objects.create(name="Desserts")
        self.assertEqual(str(category), "Desserts")

    def test_get_default_recipe_category(self):
        """Test the get_default_recipe_category function"""
        # First, ensure the 'Others' category doesn't exist
        RecipeCategory.objects.filter(name="Others").delete()

        # Call the function
        default_category = get_default_recipe_category()

        # Check if the returned category is named 'Others'
        self.assertEqual(default_category.name, "Others")

        # Call the function again to test if it returns the existing 'Others' category
        second_call = get_default_recipe_category()
        self.assertEqual(default_category, second_call)

        # Verify only one 'Others' category was created
        others_count = RecipeCategory.objects.filter(name="Others").count()
        self.assertEqual(others_count, 1)

    def test_recipe_str(self):
        """Test the string representation of Recipe"""
        self.assertEqual(str(self.recipe1), "Test Recipe 1")

    def test_recipe_like_str(self):
        """Test the string representation of RecipeLike"""
        self.assertEqual(str(self.recipe_like), "testuser")

    def test_delete_recipe(self):
        self.client.force_authenticate(user=self.user)
        # DELETE request to delete the recipe
        response = self.client.delete(self.detail_url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the recipe was deleted
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=self.recipe1.id)
    
    
    def test_like_recipe(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        RecipeLike.objects.filter(user=self.user, recipe=self.recipe1).delete()

        # POST request to like the recipe
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        like = RecipeLike.objects.filter(user=self.user, recipe=self.recipe1).first()
        self.assertIsNotNone(like)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RecipeLike.objects.filter(user=self.user, recipe=self.recipe1).count(), 1)

    def test_unlike_recipe_without_like(self):
        self.client.force_authenticate(user=self.user)
        RecipeLike.objects.filter(user=self.user, recipe=self.recipe1).delete()
        response = self.client.delete(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
          
    def test_unlike_recipe(self):
        # Authenticate the user and like the recipe first
        self.client.force_authenticate(user=self.user)
        self.client.post(self.like_url)  # Like the recipe

        # DELETE request to unlike the recipe
        response = self.client.delete(self.like_url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the like was removed
        self.assertFalse(RecipeLike.objects.filter(user=self.user, recipe=self.recipe1).exists())

    def test_like_recipe_by_other_user(self):
        # Authenticate a different user
        self.client.force_authenticate(user=self.other_user)
        RecipeLike.objects.filter(user=self.other_user, recipe=self.recipe1).delete()
        # POST request to like the recipe
        response = self.client.post(self.like_url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the like was created for the other user
        self.assertTrue(RecipeLike.objects.filter(user=self.other_user, recipe=self.recipe1).exists())

    def test_unlike_recipe_not_liked(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # DELETE request to unlike the recipe without liking it first
        response = self.client.delete(self.like_url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that no like was created
        self.assertFalse(RecipeLike.objects.filter(user=self.user, recipe=self.recipe1).exists())
        
        
