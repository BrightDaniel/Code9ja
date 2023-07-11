# Code9ja E-Learning Platform

![banner](https://github.com/BrightDaniel/Code9ja/assets/107191784/7154f600-8019-447b-acb8-07a54661e863)



Code9ja is an e-learning platform designed to provide users with an opportunity to learn coding and other tech-related courses in Nigerian Pidgin. The platform offers a wide range of courses, blog posts, and a user-friendly interface to enhance the learning experience. With Code9ja, users can apply for courses, track their application status, access the latest tech-related blog posts, and interact with the admin through the contact page.

## Features

- **User Dashboard:** Users have access to a personalized dashboard where they can view the status of their course applications. The dashboard provides an overview of applied courses, application status, and important notifications.

- **Admin Dashboard:** The admin dashboard offers administrative capabilities, allowing the admin to manage courses, quizzes (in development), blog posts, and user applications. The admin can add new courses, edit existing courses, accept/reject user applications, and perform various administrative tasks.

- **Course Management:** The admin can easily add new courses, provide detailed information about each course, set application deadlines, and manage course content. Users can browse and apply for courses directly from the platform.

- **Blog Posts:** Code9ja features a collection of tech-related blog posts that users can explore. These blog posts cover a wide range of topics and provide valuable insights and knowledge for the users.

- **Application Status:** Users can track the status of their course applications through the user dashboard. The status can be "Pending," "Paid," or "Cancelled," depending on the admin's decision.

- **Contact Page:** Code9ja offers a contact page where users can reach out to the admin for inquiries, support, or general feedback. Users can fill out a contact form and expect a response from the admin.

## Website Sections

- **Admin Area:** The admin area provides access to the admin dashboard, where administrative tasks can be performed. The admin can manage courses, blog posts, user applications, and other administrative functions.

- **User Area:** The user area is dedicated to registered users. Users can access their personalized dashboard, view course applications, track application status, and interact with the platform.

- **Public Area:** The public area of the website is accessible to everyone. It includes landing pages, the blog section, and the contact page. Users can explore the available courses, read blog posts, and get in touch with the admin through the contact page.

## Work in Progress

Code9ja is an ongoing project, and there are several features and enhancements planned for the future. Some of the upcoming features include:

- **Assessment Tests:** Implementation of assessment tests to evaluate the knowledge and progress of the users.

- **Payment Features:** Integration of payment gateways to facilitate course payments and improve the overall user experience.

- **Expanded User Registration and Application:** Enhancements to the user registration and application process to provide more comprehensive information and streamline the application workflow.

- **Collaboration and Open Source:** Code9ja welcomes collaboration and is an open-source project. Developers can contribute to the project, suggest improvements, and help shape the future of the platform.

## Technologies Used

Code9ja is built using the following technologies:

- **Python Flask:** A Python web framework used for developing the back-end of the platform.

- **MySQL:** A relational database management system used for storing application and user data.

- **HTML, CSS, JavaScript:** Front-end technologies used for designing and creating the user interface.

- **Bootstrap:** A popular CSS framework that provides responsive design and pre-built components to enhance the visual appearance of the platform.

- **FontAwesome:** A comprehensive icon set used to add visually appealing icons to the platform.

- **SCSS:** A CSS preprocessor that improves code maintainability and provides additional features such as variables and mixins.

## Deployment

Code9ja is currently hosted on Heroku, providing easy access and availability for users. The hosted version of Code9ja can be found [here](https://code9ja-cb567a167dcd.herokuapp.com/). 

## Run Locally

Code9ja can be run on your local machine by following these steps:

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/BrightDaniel/Code9ja.git
   ```

2. Navigate to the project directory:

   ```
   cd Code9ja
   ```

3. Create a virtual environment:

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:

     ```
     venv\Scripts\activate
     ```

   - For macOS and Linux:

     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

6. Set up the database:

   - Create a MySQL database for the project.

   - Update the database configuration in the `.env` file with your database details:

     ```python
     DB_URI=mysql://username:password@localhost/database_name
     ```

7. Run the database migrations:

   ```
   flask db upgrade
   ```

8. Start the development server:

   ```
   flask run --debug
   ```

9. Open your web browser and visit `http://localhost:5000` to access the Code9ja platform.

Note: Make sure you have Python, MySQL, and pip installed on your machine before running the above commands.



## Screenshots

Here are some screenshots of key pages within the Code9ja platform:

- Homepage

![homepage](https://github.com/BrightDaniel/Code9ja/assets/107191784/2f2704c7-457f-465b-a0eb-68d371ec82e0)


- User Dashboard

![user dashboard](https://github.com/BrightDaniel/Code9ja/assets/107191784/775a5cc8-c419-4295-a3cd-ab34c16594dd)



- Admin Dashboard

![admin dashboard](https://github.com/BrightDaniel/Code9ja/assets/107191784/df03b55b-04cc-4374-a3f2-33df5868d93d)



- Course Page

![courses](https://github.com/BrightDaniel/Code9ja/assets/107191784/57c09ec8-5da2-4a22-926c-a1d401964632)


- Blog Page

![blog](https://github.com/BrightDaniel/Code9ja/assets/107191784/c6676658-bb44-433d-92df-7aed7bc42cba)


- Contact Page

![contact page](https://github.com/BrightDaniel/Code9ja/assets/107191784/29644b26-c537-4fa8-b936-5c574f906a22)



## Authors and Credits

Code9ja is developed by [Bright Daniel]. We would like to express our gratitude to the open-source community and peers for their valuable contributions and support in making Code9ja a reality.

## Contributing

Code9ja welcomes contributions from the developer community. If you're interested in contributing to the project, please send a mail to the [Bright Daniel](brightdaniel5050@gmail.com) for more information.

## License

Code9ja is released under the [MIT License](LICENSE). Please refer to the License file for more details.

---

We hope you enjoy using Code9ja and find it valuable for your learning journey. If you have any questions, feedback, or suggestions, please feel free to reach out to us through the contact page on the platform. Happy learning!

