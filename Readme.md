# Web-Page-Summarization
Summarize the layout of a web page so that a screen reader reads on a high level, giving a blind user an overview of the layout w.r.t select objects on the web page.

All the required files are in the extension folder.

Trained transformer model: https://drive.google.com/drive/folders/1BgHNtUjdnz41X_wfX3X4HkM5XMusjpli?usp=sharing

Output video: https://youtu.be/6hPsRIknGkY


# Requirements:
Note: These are for the Python portion of the work and assume that the Python with version compatible with the following requirements is already installed.

Flask==2.2.2<br />
Flask_Cors==3.0.10<br />
gTTS==2.3.0<br />
ipython==8.7.0<br />
mutagen==1.46.0<br />
pandas==1.4.1<br />
pygame==2.1.2<br />
pywinauto==0.6.8<br />
selenium==4.7.2<br />
torch==1.13.0<br />
transformers==4.21.2<br />
sentencepiece==0.1.97<br />
wget==3.2<br />

# Directions:
Note: These steps are with respect to VSCode IDE and assume Python with version compatible with the requirements is already installed.


1) Install the required libraries and frameworks.
2) Run the app.py file using python -m flask run to start the server and copy the address.


Steps used for testing the API before installing the extension:

3) If not installed, install live server plugin in VSCode.
4) Once installed, click 'Go Live' which should be found close to the bottom right corner of the IDE.
5) Run app.py with 'python -m flask run' command

Steps to install the extension:

Note: This assumes that the latest version of the Google Chrome (complies with manifest version 3) is already installed.

3) On chrome, go to the Customize and control options, which can be found at the top right corner of the window under close button.
4) Go to more tools -> Extensions.
5) Make sure that the 'Developer Mode' is turned on, in the top-right region of the window.
6) Select 'Load Unpacked' and select the 'Extension' folder(remove double-underscore files from the folder if any before this step).
7) The extension should now be ready to use.

# Introduction

Most devices like computer or smartphone use a screen as the main medium to convey information to the user. As the screen is used to convey information visually, the devices by themselves are not usable for the blind. The ability to access information is called accessibility, and the information that cannot be accessed, like in this scenario, are considered inaccessible, which is an undesirable state and is considered a problem. In order to solve this problem, the screenreader is introduced. A screenreader is an assistive technology which, as the name says, reads the content on the screen. In other words, it converts the output from visual to audio, making the content on the devices accessible to a blind user.
When a general user browses the web, most of the content is perceived through vision, as it is accessed through devices whose main mode of interaction is the screen. As a result, most of the websites employ designs and layouts with visual appeal and  vision-based ease of use in mind. In this case, the content can be accessible through a screenreader, but these changes which are meant to give more comfort and satisfaction for a user in achieving his goal, have little to no effect in improving the satisfaction of a blind user. In fact, the additional elements on the web page make the situation worse for a blind user. The comfort and satisfaction experienced by a user while accessing the information he needs, is called usability. In the situation mentioned earlier, the usability of a general user is improved significantly but for a blind user there hasn't been any improvement. While accessiblity is associated with being able to obtain information, usability is associated with how comfortably the information is obtained. These decide the overall experience of a user in accessing the information, which is called user experience, in short.

In recent years, there has been significant changes to website design, like the Responsive Web Design, that lets the layout of a website adapt to different screen sizes, allowing one website to be viewed on different devices instead of sending users to different websites basing on the deviceBryant2012, but good user experience for the blind still remains elusive. Although there are some web sites that do take the blind into consideration and produce designs that comply with the accessiblity guidelines, the compliance by itself does not have significant impact on the user experiencenogueira2017evaluating. According to a studypower2012guidelines conducted on 32 blind users, the success criteria of Web Content Accessibility Guidelines (WCAG) 2caldwell2008web, the guidelines published by the World Wide Web Consortium for web accessibility, account for only 50.4\% of the challenges faced by the blind users.

While there are assistive technologies like screenreader available for a blind user to browse a web page, it may improve the accessibility of a web page but not the usability, as the audio output cannot convey information as effeciently as visual output for three main reasons - 1) Unlike visual, audio is sequential, 2) Audio cannot convey as much detail as visual and 3) It is just not possible to show some visual information in audio, like colors (A screenreader may read out the name of a color, but it is not the same as perceiving the color), patterns and designs, abstract art, etc. As a result, it is still difficult for the user to navigate a web page or understand the information, especially in this age of information overload, where web sites have huge amounts of information.

The purpose of this work is to provide a summary of the objects on a web page (like search, filters, etc.) with respect to select objects, to give the blind user a 'mental picture' of the layout of the current web page being shown and the tasks they can perform on the page.  This allows the assistive technology to present the information required for a blind user to decide his/her next action more easily, improving the usability and user experience significantly. For example, in an experiment of ours, we used NVDA, a popular screenreader, to browse a webpage on Expedia (Fig 1), a travel website. We first had to listen to the title information on the tab, then the Expedia logo followed by the 'more travel' drop down menu and the other links like language that are on the top right corner of the window, then the going to, check-in and check-out are read out as headings which are again read out as buttons. By the time we arrived at the search button, it took around 58 seconds, during which time, a user with good vision would have been able to accomplish much more, making the difference in the usability evident.

To bridge this gap in usability, unlike most papers related to web summarization, which are focused on summarizing a product or service offered on a web page (like Mabrouk et al marbouk2021), to help the users in activities like making decisions related to the product or service, this work is provides an overview of the webpage so that a blind user gets an idea of where to find the search button (or any other important object on the website) much sooner, and can navigate to that area directly, without having to go through each detail.

