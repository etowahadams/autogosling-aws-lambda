# AutoGosling in AWS Lambda

This is an AWS Lambda function which takes an image of a genomics visualization and returns a [Gosling specification](http://gosling-lang.org/docs/reference) 
which approximates the input visualization. Most of the code was copied and adapted from [AutoGosling](https://github.com/autogosling/autogosling-tool).

`app.py` is the entry point for the lambda function.

## Local development
### Setup
Tested using Python 3.9. 
```bash
git clone https://github.com/etowahadams/autogosling-aws-lambda.git
cd autogosling-aws-lambda
## Create a virtual environment
python -m venv env
source env/bin/activate
pip install -r requirements.txt
## Download the ONNX model
wget -O best.onnx https://drive.google.com/file/d/1x_e4V9LDgjsZhMWCnONbiQXK4Zfw6t27/view?usp=share_link
```
### Test usage
This will return the predicted Gosling specification 
```bash
python3 main.py glyph.png
```