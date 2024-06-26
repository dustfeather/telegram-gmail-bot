from setuptools import setup, find_packages

setup(
    name="telegram-gmail-bot",
    version="0.1.16",
    author="Catalin Teodorescu",
    author_email="dustfeather@gmail.com",
    description="A bot that connects Telegram with Gmail",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/dustfeather/telegram-gmail-bot",
    packages=find_packages(),
    install_requires=[
        'anyio==4.4.0',
        'cachetools==5.3.3',
        'certifi==2024.2.2',
        'charset-normalizer==3.3.2',
        'google-api-core==2.19.0',
        'google-api-python-client==2.130.0',
        'google-auth==2.29.0',
        'google-auth-httplib2==0.2.0',
        'google-auth-oauthlib==1.2.0',
        'googleapis-common-protos==1.63.0',
        'h11==0.14.0',
        'httpcore==1.0.5',
        'httplib2==0.22.0',
        'httpx==0.27.0',
        'idna==3.7',
        'oauthlib==3.2.2',
        'proto-plus==1.23.0',
        'protobuf==4.25.3',
        'pyasn1==0.6.0',
        'pyasn1_modules==0.4.0',
        'pyparsing==3.1.2',
        'python-dotenv==1.0.1',
        'python-telegram-bot==21.2',
        'requests==2.32.2',
        'requests-oauthlib==2.0.0',
        'rsa==4.9',
        'sniffio==1.3.1',
        'tenacity==8.3.0',
        'uritemplate==4.1.1',
        'urllib3==2.2.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'telegram-gmail-bot=telegram_gmail_bot:main',
        ],
    },
)
