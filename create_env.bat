@echo off

REM Set the name of your new conda environment
SET ENV_NAME=my_langchain_env

REM Create a new conda environment, with python 3.8
conda create --yes --name %ENV_NAME% python=3.8

REM Activate the new environment
conda activate %ENV_NAME%

REM Install the required dependencies
pip install langchain transformers pandas datasets faiss-cpu

REM Print successful installation message
echo.
echo Dependencies installed in the new conda environment: %ENV_NAME%
echo.

pause