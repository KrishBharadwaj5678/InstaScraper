import instaloader
import streamlit as st
import shutil
import requests

st.set_page_config(
    page_title="Instagram Scraper",
    page_icon="icon.png",
    menu_items={
        "About":"Insta Scraper provides a powerful and user-friendly platform for downloading and scraping Instagram content. Whether you want to download posts, highlights, or reels, or scrape detailed profile information, our tool offers a seamless experience. Simply enter the required details, and get your content in a zip file or detailed profile data quickly and efficiently."
    }
)

st.write("<h2 style='color:hotpink;'>Download and Scrape Instagram Content.</h2>",unsafe_allow_html=True)

L = instaloader.Instaloader()

L = instaloader.Instaloader(
    download_videos=True,    
    download_pictures=True,  
    post_metadata_txt_pattern='abc.txt'  
)

tab1,tab2,tab3,tab4=st.tabs(["Download Posts","Download Highlights","Download Reel","Scrape Profile"])

def auth(key1,key2,key3):
    usrname=st.text_input("Username",placeholder="Your Instagram Username",key=key1)
    password=st.text_input("Password",type="password",placeholder="Your Instagram Password",key=key2)
    prof_name=st.text_input("Target",placeholder="Specify Target Username",key=key3)
    return [usrname,password,prof_name]

with tab1:
    [username,password,prof_name]=auth(10,20,30)
    btn=st.button("Generate",key=1)
    if btn:
        try:
            with st.spinner("This may take few minutes..."):
                    L.login(username.strip(), password.strip())

                    L.download_profile(prof_name.strip(), profile_pic_only=False,download_stories=True,download_tagged=True,fast_update=True)

                    shutil.make_archive(f"{prof_name}",'zip', prof_name)
                    with open(f"{prof_name}.zip","rb") as file:
                        st.download_button("Download",file,f"{prof_name}.zip")
        except:
            st.error("Something Went Wrong!")

with tab2:
      [username,password,prof_name]=auth(70,80,90)
      btn=st.button("Generate",key=2)
      if btn:
            try:
               with st.spinner("This may take few minutes..."):
                L.login(username.strip(), password.strip())
                profile = instaloader.Profile.from_username(L.context, prof_name.strip())
                L.download_highlights(profile, fast_update=True) 

                shutil.make_archive(f"{prof_name}_highlights",'zip', f"{prof_name}")
                with open(f"{prof_name}_highlights.zip","rb") as file:
                        st.download_button("Download",file,f"{prof_name}_highlights.zip")
            except:
                st.error("Something Went Wrong!")

with tab3:
    url=st.text_input("Reel URL",placeholder="Paste Link Here...")
    btn=st.button("Generate",key=3)
    if btn:
        try:
            shortcode=url.split("/")[5].strip()
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target='reels')
            
            shutil.make_archive(f"reels_{shortcode}",'zip', f"reels")
            with open(f"reels_{shortcode}.zip","rb") as file:
                        st.download_button("Download",file,f"reels_{shortcode}.zip")
        except:
            st.error("Something Went Wrong!")

with tab4:
    target=st.text_input("Username",placeholder="Specify Username")
    btn=st.button("Generate",key=4)
    if btn:
        try:
              with st.spinner("This may take few seconds..."):
                profile = instaloader.Profile.from_username(L.context, target.strip())
                profile_info = {
                    'username': profile.username,
                    'fullname': profile.full_name,
                    'bio': profile.biography,
                    'profile_pic_url': profile.profile_pic_url,
                    'followers_count': profile.followers,
                    'following_count': profile.followees,
                    'total_posts': profile.mediacount,
                    'is_private': profile.is_private,
                    'is_verified': profile.is_verified,
                    'is_business_account': profile.is_business_account
                }

                response = requests.get(profile_info['profile_pic_url'])

                with open("user_image.jpg","wb+") as img:
                    img.write(response.content)

                st.write(f"<li style='font-size:29px;color:lightgreen;'>Profile Pic:</li>",unsafe_allow_html=True)
            
                st.image("user_image.jpg",width=200)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Username: {profile_info['username']}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Full Name: {profile_info['fullname']}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Bio: {profile_info['bio']}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Followers: {profile_info['followers_count']}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Following: {profile_info['following_count']}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Total Posts: {profile_info['total_posts']}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Private Profile: {'Yes' if profile_info['is_private'] else 'No'}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Verified Profile: {'Yes' if profile_info['is_verified'] else 'No'}</li>",unsafe_allow_html=True)

                st.write(f"<li style='font-size:27px;color:lightgreen;'>Business Account: {'Yes' if profile_info['is_business_account'] else 'No'}</li>",unsafe_allow_html=True)
        except:     
            st.error("Something Went Wrong!")
