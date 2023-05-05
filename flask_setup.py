from flask import Flask, render_template, redirect, request, url_for, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asasdasdjhslkjsbduijbqwdbjx23ljbk32jeo2ip3iuv'
