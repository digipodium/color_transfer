import os
import streamlit as st

from db import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


st.title("Color Transfer App")

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_file(file,path):
    try:
        db = opendb()
        ext = file.type.split('/')[1] # second piece
        img = Image(filename=file.name,extension=ext,filepath=path)
        db.add(img)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False




choice = st.sidebar.selectbox("select option",['view uploads','upload content','manage uploads'])

if choice == 'upload content':
    file = st.file_uploader("select a image",type=['jpg','png'])
    if file:
        path = os.path.join('uploads',file.name)
        with open(path,'wb') as f:
            f.write(file.getbuffer())
            status = save_file(file,path)
            if status:
                st.sidebar.success("file uploaded")
                st.sidebar.image(path,use_column_width=True)
            else:
                st.sidebar.error('upload failed')

if choice == 'view uploads':
    db = opendb()
    results = db.query(Image).all()
    db.close()
    img = st.sidebar.radio('select image',results)
    if img and os.path.exists(img.filepath):
        st.sidebar.info("selected img")
        st.sidebar.image(img.filepath, use_column_width=True)
        if st.sidebar.button("analyse"):
            st.title(f"{img.filename} to be continued")
        

if choice == 'manage uploads':
    db = opendb()
    # results = db.query(Image).filter(Image.uploader == 'admin') if u want to use where query
    results = db.query(Image).all()
    db.close()
    img = st.sidebar.radio('select image to remove',results)
    if img:
        st.error("img to be deleted")
        if os.path.exists(img.filepath):
            st.image(img.filepath, use_column_width=True)
        if st.sidebar.button("delete"): 
            try:
                db = opendb()
                db.query(Image).filter(Image.id == img.id).delete()
                if os.path.exists(img.filepath):
                    os.unlink(img.filepath)
                db.commit()
                db.close()
                st.info("image deleted")
            except Exception as e:
                st.error("image not deleted")
                st.error(e)