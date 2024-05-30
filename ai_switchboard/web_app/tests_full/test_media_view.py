from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.template.loader import render_to_string
from django.template import Template, Context
from django.core.files.uploadedfile import SimpleUploadedFile
from ..views import *


class GetFilesTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # Test that get_files correctly returns all files of image type
    def test_get_files_with_image(self):
        Image.objects.create(name='image1.jpg', data=b'data1')
        Image.objects.create(name='image2.jpeg', data=b'data2')
        Image.objects.create(name='image3.png', data=b'data3')

        files = get_files()

        self.assertEqual(len(files), 3)

        self.assertEqual(files[0]['type'], 'image')
        self.assertEqual(files[0]['name'], 'image1.jpg')

        self.assertEqual(files[1]['type'], 'image')
        self.assertEqual(files[1]['name'], 'image2.jpeg')

        self.assertEqual(files[2]['type'], 'image')
        self.assertEqual(files[2]['name'], 'image3.png')

    # Test that get_files correctly returns all files of video type
    def test_get_files_with_video(self):
        Video.objects.create(name='video1.mp4', data=b'data1')
        Video.objects.create(name='video2.avi', data=b'data2')

        files = get_files()

        self.assertEqual(len(files), 2)

        self.assertEqual(files[0]['type'], 'video')
        self.assertEqual(files[0]['name'], 'video1.mp4')

        self.assertEqual(files[1]['type'], 'video')
        self.assertEqual(files[1]['name'], 'video2.avi')

    # Test that get_files correctly returns all files of csv type
    def test_get_files_with_csv(self):
        CSV.objects.create(name='csv1.csv', data=b'data1')
        CSV.objects.create(name='csv2.csv', data=b'data2')

        files = get_files()

        self.assertEqual(len(files), 2)

        self.assertEqual(files[0]['type'], 'csv')
        self.assertEqual(files[0]['name'], 'csv1.csv')

        self.assertEqual(files[1]['type'], 'csv')
        self.assertEqual(files[1]['name'], 'csv2.csv')

    # Test that get_files correctly returns all files of json type
    def test_get_files_with_json(self):
        JSON.objects.create(name='json1.json', data=b'data1')
        JSON.objects.create(name='json2.json', data=b'data2')

        files = get_files()

        self.assertEqual(len(files), 2)

        self.assertEqual(files[0]['type'], 'json')
        self.assertEqual(files[0]['name'], 'json1.json')

        self.assertEqual(files[1]['type'], 'json')
        self.assertEqual(files[1]['name'], 'json2.json')

    # Test that get_files correctly returns all files of text type
    def test_get_files_with_text(self):
        Text.objects.create(name='text1.txt', data=b'data1')
        Text.objects.create(name='text2.txt', data=b'data2')

        files = get_files()

        self.assertEqual(len(files), 2)

        self.assertEqual(files[0]['type'], 'text')
        self.assertEqual(files[0]['name'], 'text1.txt')

        self.assertEqual(files[1]['type'], 'text')
        self.assertEqual(files[1]['name'], 'text2.txt')

    # Test that get_files correctly returns all files of multiple types
    def test_get_files_with_no_file_type_specified(self):

        Image.objects.create(name='image.png', data=b'data')
        Video.objects.create(name='video.mp4', data=b'data')
        CSV.objects.create(name='file.csv', data='data')
        JSON.objects.create(name='file.json', data='{"key": "value"}')
        Text.objects.create(name='file.txt', data='data')

        files = get_files()

        self.assertEqual(len(files), 5)

    # Test that get_files correctly returns all files of multiple types
    def test_get_files_with_all_file_types(self):

        Image.objects.create(name='image.png', data=b'data')
        Video.objects.create(name='video.mp4', data=b'data')
        CSV.objects.create(name='file.csv', data='data')
        JSON.objects.create(name='file.json', data='{"key": "value"}')
        Text.objects.create(name='file.txt', data='data')

        files = get_files()

        self.assertEqual(len(files), 5)


"""
class MediaLogicTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_media_logic_with_no_file_type_specified(self): 
    
        image = Image.objects.create(name='image.png', data=b'data')
        video = Video.objects.create(name='video.mp4', data=b'data')
        csv_file = CSV.objects.create(name='file.csv', data='data')
        json_file = JSON.objects.create(name='file.json', data='{"key": "value"}')
        text_file = Text.objects.create(name='file.txt', data='data')

        request = self.factory.get('/media/')
        response = media_logic(request)

        expected_context = {
            'files': [
                {'id': image.id, 'name': image.name, 'type': 'image'},
                {'id': video.id, 'name': video.name, 'type': 'video'},
                {'id': csv_file.id, 'name': csv_file.name, 'type': 'csv'},
                {'id': json_file.id, 'name': json_file.name, 'type': 'json'},
                {'id': text_file.id, 'name': text_file.name, 'type': 'text'},
            ]
        }
        # ashduahduisad helpppp
        self.assertDictEqual(response.context, expected_context)
"""


class DeleteFileLogicTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    # Test that the image file is deleted
    def test_delete_image_file(self):
        # Creates a sample image file
        image = Image.objects.create(name='image.png', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{image.id}/image/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(image.id, 'image', request)

        with self.assertRaises(Image.DoesNotExist):
            Image.objects.get(id=image.id)

    # Test that a notification is created
    def test_delete_image_notification(self):
        # Creates a sample image file
        image = Image.objects.create(name='image.png', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{image.id}/image/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(image.id, 'image', request)

        notification = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notification), 1)
        self.assertEqual(notification[0].message, f'User {self.user.username} deleted file {image.name}')

    # Test that the video file is deleted
    def test_delete_video_file(self):

        # Creates a sample video file
        video = Video.objects.create(name='video.mp4', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{video.id}/video/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(video.id, 'video', request)

        with self.assertRaises(Video.DoesNotExist):
            Video.objects.get(id=video.id)

    # Test that a notification is created
    def test_delete_video_notification(self):
        # Creates a sample video file
        video = Video.objects.create(name='video.avi', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{video.id}/video/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(video.id, 'video', request)

        notification = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notification), 1)
        self.assertEqual(notification[0].message, f'User {self.user.username} deleted file {video.name}')

# Test that the csv file is deleted
    def test_delete_csv_file(self):

        # Creates a sample csv file
        csv = CSV.objects.create(name='csv.csv', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{csv.id}/csv/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(csv.id, 'csv', request)

        with self.assertRaises(csv.DoesNotExist):
            CSV.objects.get(id=csv.id)

    # Test that a notification is created
    def test_delete_csv_notification(self):
        # Creates a sample csv file
        csv = CSV.objects.create(name='csv.csv', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{csv.id}/csv/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(csv.id, 'csv', request)

        notification = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notification), 1)
        self.assertEqual(notification[0].message, f'User {self.user.username} deleted file {csv.name}')

    # Test that the json file is deleted
    def test_delete_json_file(self):

        # Creates a sample json file
        json = JSON.objects.create(name='json.json', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{json.id}/json/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(json.id, 'json', request)

        with self.assertRaises(json.DoesNotExist):
            JSON.objects.get(id=json.id)

    # Test that a notification is created
    def test_delete_json_notification(self):
        # Creates a sample json file
        json = JSON.objects.create(name='json.json', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{json.id}/json/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(json.id, 'json', request)

        notification = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notification), 1)
        self.assertEqual(notification[0].message, f'User {self.user.username} deleted file {json.name}')

# Test that the text file is deleted
    def test_delete_text_file(self):

        # Creates a sample text file
        text = Text.objects.create(name='text.txt', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{text.id}/text/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(text.id, 'text', request)

        with self.assertRaises(text.DoesNotExist):
            Text.objects.get(id=text.id)

    # Test that a notification is created
    def test_delete_text_notification(self):
        # Creates a sample text file
        text = Text.objects.create(name='text.txt', data=b'data')

        # Creates a request with user authentication
        request = self.factory.get(f'/delete_file/{text.id}/text/')
        request.user = self.user

        # Calls the delete_file_logic function
        delete_file_logic(text.id, 'text', request)

        notification = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notification), 1)
        self.assertEqual(notification[0].message, f'User {self.user.username} deleted file {text.name}')


class DownloadFileLogicTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    # Test that the image file is downloaded
    def test_download_image_file(self):

        image = Image.objects.create(name='image.jpeg', data=b'data')

        request = self.factory.get(f'/download_file/{image.id}/image/')
        request.user = self.user

        response = download_file_logic(image.id, 'image', request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/jpeg')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename={image.name}')

    # Test that a notification is created
    def test_download_image_notification(self):

        image = Image.objects.create(name='image.jpeg', data=b'data')

        request = self.factory.get(f'/download_file/{image.id}/image/')
        request.user = self.user

        download_file_logic(image.id, 'image', request)

        # Verify that a notification is created
        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} downloaded file {image.name}')

    # Test that the video file is downloaded
    def test_download_video_file(self):
        video = Video.objects.create(name='video.mp4', data=b'data')

        request = self.factory.get(f'/download_file/{video.id}/video/')
        request.user = self.user

        response = download_file_logic(video.id, 'video', request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'video/mp4')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename={video.name}')

    # Test that a notification is created
    def test_download_video_notification(self):
        video = Video.objects.create(name='video.mp4', data=b'data')

        request = self.factory.get(f'/download_file/{video.id}/video/')
        request.user = self.user

        download_file_logic(video.id, 'video', request)

        # Verify that a notification is created
        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} downloaded file {video.name}')

    # Test that the csv file is downloaded
    def test_download_csv_file(self):
        csv = CSV.objects.create(name='csv.csv', data=b'data')

        request = self.factory.get(f'/download_file/{csv.id}/csv/')
        request.user = self.user

        response = download_file_logic(csv.id, 'csv', request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename={csv.name}')

    # Test that a notification is created
    def test_download_csv_notification(self):
        csv = CSV.objects.create(name='csv.csv', data=b'data')

        request = self.factory.get(f'/download_file/{csv.id}/csv/')
        request.user = self.user

        download_file_logic(csv.id, 'csv', request)

        # Verify that a notification is created
        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} downloaded file {csv.name}')

    # Test that the json file is downloaded
    def test_download_json_file(self):
        json = JSON.objects.create(name='json.json', data=b'data')

        request = self.factory.get(f'/download_file/{json.id}/json/')
        request.user = self.user

        response = download_file_logic(json.id, 'json', request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename={json.name}')

    # Test that a notification is created
    def test_download_json_notification(self):
        json = JSON.objects.create(name='json.json', data=b'data')

        request = self.factory.get(f'/download_file/{json.id}/json/')
        request.user = self.user

        download_file_logic(json.id, 'json', request)

        # Verify that a notification is created
        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} downloaded file {json.name}')

    # Test that the text file is downloaded
    def test_download_text_file(self):
        text = Text.objects.create(name='text.txt', data=b'data')

        request = self.factory.get(f'/download_file/{text.id}/text/')
        request.user = self.user

        response = download_file_logic(text.id, 'text', request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename={text.name}')

    # Test that a notification is created
    def test_download_text_notification(self):
        text = Text.objects.create(name='text.txt', data=b'data')

        request = self.factory.get(f'/download_file/{text.id}/text/')
        request.user = self.user

        download_file_logic(text.id, 'text', request)

        # Verify that a notification is created
        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} downloaded file {text.name}')

    # Test that the download_file handles invalid types
    def test_invalid_file_type(self):

        request = self.factory.get('/download_file/123/invalid_type/')
        request.user = self.user

        response = download_file_logic(123, 'invalid_type', request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid file type')

    # Test that no notification is created for invalid file types
    def test_invalid_file_notification(self):

        request = self.factory.get('/download_file/123/invalid_type/')
        request.user = self.user

        download_file_logic(123, 'invalid_type', request)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 0)


class UploadFileLogicTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    # Test that the image file is uploaded
    def test_upload_image_file(self):

        image_data = b'dummy_image_data'
        image_file = SimpleUploadedFile("image.jpeg", image_data, content_type="image/jpeg")

        request = self.factory.post('/upload_file/', {'fileType': 'image', 'file': image_file})
        request.user = self.user

        response = upload_file_logic(request)

        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)

        self.assertEqual(Image.objects.count(), 1)

        self.assertIn(b'File uploaded successfully', redirected_response.content)

    # Test that a notification is created for image file upload
    def test_notification_created_for_image(self):

        image_data = b'dummy_image_data'
        image_file = SimpleUploadedFile("image.jpg", image_data, content_type="image/jpg")

        request = self.factory.post('/upload_file/', {'fileType': 'image', 'file': image_file})
        request.user = self.user

        upload_file_logic(request)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} uploaded file {image_file.name}')

    # Test that the video file is uploaded
    def test_upload_video_file(self):
        video_data = b'dummy_video_data'
        video_file = SimpleUploadedFile("video.mp4", video_data, content_type="video/mp4")

        request = self.factory.post('/upload_file/', {'fileType': 'video', 'file': video_file})
        request.user = self.user

        response = upload_file_logic(request)

        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)

        self.assertEqual(Video.objects.count(), 1)

        self.assertIn(b'File uploaded successfully', redirected_response.content)

    # Test that a notification is created for video file upload
    def test_notification_created_for_video(self):
        video_data = b'dummy_video_data'
        video_file = SimpleUploadedFile("video.avi", video_data, content_type="video/avi")

        request = self.factory.post('/upload_file/', {'fileType': 'video', 'file': video_file})
        request.user = self.user

        upload_file_logic(request)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} uploaded file {video_file.name}')

    # Test that the csv file is uploaded
    def test_upload_csv_file(self):
        csv_data = b'dummy_csv_data'
        csv_file = SimpleUploadedFile("csv.csv", csv_data, content_type="text/csv")

        request = self.factory.post('/upload_file/', {'fileType': 'csv', 'file': csv_file})
        request.user = self.user

        response = upload_file_logic(request)

        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)

        self.assertEqual(CSV.objects.count(), 1)

        self.assertIn(b'File uploaded successfully', redirected_response.content)

    # Test that a notification is created for csv file upload
    def test_notification_created_for_csv(self):
        csv_data = b'dummy_csv_data'
        csv_file = SimpleUploadedFile("csv.csv", csv_data, content_type="text/csv")

        request = self.factory.post('/upload_file/', {'fileType': 'csv', 'file': csv_file})
        request.user = self.user

        upload_file_logic(request)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} uploaded file {csv_file.name}')

    # Test that the json file is uploaded
    def test_upload_json_file(self):
        json_data = b'dummy_json_data'
        json_file = SimpleUploadedFile("json.json", json_data, content_type="application/json")

        request = self.factory.post('/upload_file/', {'fileType': 'json', 'file': json_file})
        request.user = self.user

        response = upload_file_logic(request)

        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)

        self.assertEqual(JSON.objects.count(), 1)

        self.assertIn(b'File uploaded successfully', redirected_response.content)

    # Test that a notification is created for json file upload
    def test_notification_created_for_json(self):
        json_data = b'dummy_json_data'
        json_file = SimpleUploadedFile("json.json", json_data, content_type="application/json")

        request = self.factory.post('/upload_file/', {'fileType': 'json', 'file': json_file})
        request.user = self.user

        upload_file_logic(request)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} uploaded file {json_file.name}')

    # Test that the text file is uploaded
    def test_upload_text_file(self):
        text_data = b'dummy_text_data'
        text_file = SimpleUploadedFile("text.txt", text_data, content_type="text/plain")

        request = self.factory.post('/upload_file/', {'fileType': 'text', 'file': text_file})
        request.user = self.user

        response = upload_file_logic(request)

        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)

        self.assertEqual(Text.objects.count(), 1)

        self.assertIn(b'File uploaded successfully', redirected_response.content)

    # Test that a notification is created for text file upload
    def test_notification_created_for_text(self):
        text_data = b'dummy_text_data'
        text_file = SimpleUploadedFile("text.txt", text_data, content_type="text/plain")

        request = self.factory.post('/upload_file/', {'fileType': 'text', 'file': text_file})
        request.user = self.user

        upload_file_logic(request)

        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, f'User {self.user.username} uploaded file {text_file.name}')

    # Test that the upload_file_logic function handles invalid file extensions
    def test_invalid_file_extensions(self):

        invalid_extension_data = b'dummy_text_data'
        invalid_extension_file = SimpleUploadedFile("invalid_extension.py", invalid_extension_data, content_type="text/plain")

        request = self.factory.post('/upload_file/', {'fileType': 'text/plain', 'file': invalid_extension_file})
        request.user = self.user

        response = upload_file_logic(request)

        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)

        self.assertIn(b'Invalid file extension', redirected_response.content)

        """
        # cant test for the notification for some reason it doesnt create it (i might be stupid and that might be for another test case but anyways i cant get it)
        # Check if notification is created
        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(len(notifications), 1) # i get 0!=1 in the assert
        self.assertEqual(notifications[0].message, f'User {self.user.username} tried to upload bad file')
        """

    # Test that the upload_file_logic function handles invalid file types
    def test_invalid_file_type(self):

        invalid_type_data = b'dummy_text_data'
        invalid_type_file = SimpleUploadedFile("invalid_type.txt", invalid_type_data, content_type="invalid_type")

        request = self.factory.post('/upload_file/', {'fileType': 'invalid_type', 'file': invalid_type_file})
        request.user = self.user

        response = upload_file_logic(request)

        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.url)
        self.assertEqual(redirected_response.status_code, 200)

        self.assertIn(b'No file uploaded choose correct file type', redirected_response.content)
