# coding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, request, render_template, url_for, redirect, abort, jsonify
import logging
import os

from scipy.misc import imresize, imread
import numpy as np
from tensorflow import make_tensor_proto
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc
import grpc

app = Flask(__name__)
# app.config['DEBUG'] = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

basedir = os.path.abspath(os.path.dirname(__file__))
path = basedir + "/static/photo/"


@app.route('/hi')
def hello_world():
    logger.info('in hello function')
    return 'Hello World!'


@app.route('/index')
def index():
    logger.info('in index function')
    return render_template('index.html')


@app.route('/')
def predict():
    logger.info('in predict function')
    return render_template('predict.html')


@app.route('/ajax_upload', methods=['POST'])
def ajax_upload():
    status = 'success'
    detail = ''
    logger.info('in ajax upload function')
    if request.method == 'POST' and 'file_data' in request.files:
        img = request.files.get('file_data')
        img.save(path + img.filename)
    else:
        status = 'error'
        detail = 'image file upload error.'
    msg = {
        'status': status,
        'detail': detail,
        'image_path': (path + img.filename) if status == 'success' else '',
    }
    return jsonify(msg)


@app.route('/classify', methods=['POST'])
def doclassify():
    logger.info('in doClassify function')
    filename = request.form['filename']
    server = request.form['grpc_server_ip']
    port = request.form['grpc_server_port']
    timeout = request.form['grpc_timeout']

    status, msg = 'success', ''

    try:
        r = classify(path + filename, server, port, timeout)
    except grpc.RpcError as err:
        status = 'error'
        if err.code() == grpc.StatusCode.UNAVAILABLE:
            msg = 'connect failed.'
    except Exception as err:
        status = 'error'
        msg = 'grpc error: '+err.code()

    tuple_list, new_tlist = [], []

    if status == 'success':
        scores = r.outputs['scores'].float_val
        lables = r.outputs['labels'].string_val

        for i in range(len(scores)):
            print(i, scores[i])
            tuple_list.append({'k': lables[i], 'v': scores[i]})
        new_tlist = sorted(
            tuple_list,
            cmp=lambda x, y: cmp(x['v'], y['v']), reverse=True)

    result = {'data': new_tlist, 'status': status, 'message': msg}
    return jsonify(result)


def classify(file_path, _server, _port, _timeout):
    host = _server if _server else app.config['grpc_server']
    port = _port if _port else app.config['grpc_port']
    grpc_timeout = _timeout if _timeout else app.config['grpc_timeout']

    img_height = app.config['img_height']
    img_width = app.config['img_width']
    input_mean = app.config['input_mean']
    input_std = app.config['input_std']

    print('timeout:{}'.format(grpc_timeout))

    model_name = app.config['model_name']
    model_signature_name = app.config['model_signature_name']

    # image = img
    image = imread(file_path)
    image = imresize(image, [img_height, img_width])
    image = image.astype(np.float32)
    image = (image - input_mean) / input_std
    # image = image.ravel()
    images = np.expand_dims(image, 0)

    channel = grpc.insecure_channel('{}:{}'.format(host, port))
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name  # 'cat-prediction'
    request.model_spec.signature_name = model_signature_name  # 'predict_images'

    request.inputs['images'].CopyFrom(
        make_tensor_proto(
            images, shape=[
                1, img_height, img_width, 3]))

    result = stub.Predict(request, float(grpc_timeout))  # 60 secs timeout

    return result


# def predict(kwargs):
#     import tensorflow as tf
#     host = kwargs['host']
#     port = kwargs['port']
#     file_name = kwargs['file_name']
#     input_height = 224
#     input_width = 224
#     input_mean = 128
#     input_std = 128
#     file_reader = tf.read_file(file_name)
#
#     image_reader = tf.image.decode_jpeg(
#         file_reader, channels=3, name='jpeg_reader')
#     float_caster = tf.cast(image_reader, tf.float32)
#     dims_expander = tf.expand_dims(float_caster, 0)
#     resized = tf.image.resize_bilinear(
#         dims_expander, [input_height, input_width])
#     normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
#     sess = tf.Session(target='{}:{}'.format(host, port))
#     result = sess.run(normalized)
#     return result

#
# @app.route('/upload', methods=['POST'])
# def upload():
#     logger.info('in upload function')
#     if request.method == 'POST' and 'file' in request.files:
#         img = request.files.get('file')
#         path = basedir + "/static/photo/"
#         img.save(path + img.filename)
#         # do classify
#         r = classify(path + img.filename)
#         print('show result\n:{}'.format(r))
#         return redirect(url_for('show', name=img.filename))
#     return render_template('index.html')
#
#
# @app.route('/photo/<name>')
# def show(name):
#     if name is None:
#         abort(404)
#
#     path = "../static/photo/"
#     # url = photos.url(name)
#     return render_template('show.html', url=path + name, name=name)
#

if __name__ == '__main__':
    app.run()
