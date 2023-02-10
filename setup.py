import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="work-tracker",
        author="Brian Fouts",
        author_email="brian.e.fouts@gmail.com",
        python_requires=">=3.12,<3.13",
        install_requires=[
            "Django==4.1.6",
            "psycopg2",
            "djangorestframework",
            "djangorestframework-simplejwt[crypto]",
        ],
        extras_require={
            "dev": {"pytest", "isort", "black", "pytest-django", "flake8"},
            "client": {"requests"},
        },
    )
