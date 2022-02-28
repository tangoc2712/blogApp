# Blog 2.0

_This is blog webapp 2.0 using Django, basic HTML, CSS, Boostrap_

You can see at [Học nhạc cùng KiKi](https://tqn-blog.herokuapp.com/)

## 1. Installation

-   Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all package.

    ```bash
    pip install virtualenv
    virtualenv <yourFoldername>
    cd <yourFoldername>

    # in Window OS, activate virtualenv
    scripts\activate
    ```

-   Use the [git](https://git-scm.com/) to install project.

    ```bash
    git clone github.com/tangoc2712
    cd mysite
    pip install -r requirement.txt
    ```

## 2. Run project

_Create superuser for admin site, migrate to create database_

```bash
python manage.py createsuperuser
python manage.py migrate
python manage.py runserver
```

After that, run in browser by default [127.0.0.1:8000](127.0.0.1:8000)

## 3. More description in Vietnamese

-   [Docs](https://github.com/tangoc2712/blogApp/blob/main/docs.md) 

## 4. Preview
Home Page, Comment Function

 ![](https://github.com/tangoc2712/blogApp/blob/main/image/full.jpeg?raw=true)
 
Search Function

 ![](https://github.com/tangoc2712/blogApp/blob/main/image/search.jpeg?raw=true)
 
Share Function

 ![](https://github.com/tangoc2712/blogApp/blob/main/image/share.jpeg?raw=true)

## 5. License

-   [MIT](https://choosealicense.com/licenses/mit/)
