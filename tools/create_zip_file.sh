export VIRTUALENV='steel_eye_env'
export ZIP_FILE='lambda.zip'
export PYTHON_VERSION='python3.6'

# Zip dependencies from virtualenv, and main.py
cd $VIRTUALENV/lib/$PYTHON_VERSION/site-packages/
zip -r9 ../../../../$ZIP_FILE *
cd ../../../../
zip -g $ZIP_FILE main.py