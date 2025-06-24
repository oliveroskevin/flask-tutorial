from langchain_aws import ChatBedrockConverse
from flask import Blueprint, request, render_template
import os
import boto3

llm_bp = Blueprint('llm_bp', __name__, template_folder='../templates', static_folder='../static')

@llm_bp.route('/aws-bedrock', methods=['POST'])
def aws_bedrock():
    if request.method == 'POST':
        request_data = request.get_json()
        print(os.getenv('AWS_REGION'))
        bedrock_client = boto3.client(
                "bedrock-runtime",
                region_name=os.getenv('AWS_REGION'),
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_ID'),
        )
        llm = ChatBedrockConverse(
            model="anthropic.claude-3-haiku-20240307-v1:0",
                temperature=1,
                max_tokens=4096,
                region_name=os.getenv('AWS_REGION'),
                client=bedrock_client,
        )
        messages = [
            ("system", "You are a helpful assistant."),
            ("human", request_data.get("message"))
        ]
        response = llm.invoke(messages)
        return {
            "response": response.content
        }
    else:
        return render_template('chatbot.html')