from setuptools import setup

setup(
    name="pyalgdb",
    version="0.0.1",    
    packages=["pyalgdb", "pyalgdb.src"],
    author=("Henrique Linhares"),
    author_email="hlinhares@id.uff.br",
    description="",
    entry_points={
        "console_scripts": ["pyalgdb=pyalgdb.src.mn:main"]
    },
    keywords=[""],
    url="",
    python_requires='>=3.5',
    classifiers=[
    	'Development Status :: 3 - Alpha',
    	'License :: OSI Approved :: MIT License',
    	'Programming Language :: Python :: 3.5',
    	'Programming Language :: Python :: 3.6',
    ],
)