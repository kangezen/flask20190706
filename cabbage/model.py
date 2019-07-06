import tensorflow as tf
import pandas as pd
import numpy as np

class CabbaageModel:
    def __init__(self):
        pass

    def create_model(self):
        model = tf.global_variables_initializer()
        data = pd.read_csv('./data/price_data.csv', sep=',')
        xy = np.array(data,dtype=np.float)
        x_data = xy[:, 1:-1] # feature
        y_data = xy[:, [-1]] # 가격

        # 대문자는 확률 변수, 소문자는 그냥 변수
        # 확률 변수 X(1,2,3,4) 1이 들어갈 수도 있고, 2가 들어갈 수도 있고, 3이 들어 ...., 그냥 변수 x =1

        # 플레이스홀더 설정
        X = tf.placeholder(tf.float32, shape=[None, 4])
        Y = tf.placeholder(tf.float32, shape=[None,1])
        W = tf.Variable(tf.random_normal([4,1]), name='weight')
        b = tf.Variable(tf.random_normal([1]), name='bias')

        # 가설 설정
        # Y = wx + b
        hypothesis = tf.matmul(X, W) + b

        # 비용함수 설정      #비용함수 : 평균에 가깝게 그은 선     #설정이란 식을 세운다는 뜻
        cost = tf.reduce_mean(tf.square(hypothesis - Y ))

        # 최적화함수 설정
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.000005)
        train = optimizer.minimize(cost)

        #세션 설정
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        # 러닝

        for step in range(100000):
            cost_, hypo_, _ = sess.run([cost, hypothesis, train], feed_dict={X: x_data, Y: y_data})
            if step % 5000 == 0:
                print("# %d 손실비용 : %d" % (step, cost_))
                #손실비용 : 정답과의 오차
                print("- 배추가격 : %d" % (hypo_[0]))

        #  학습된 모델 저장
        saver = tf.train.Saver()
        save_path = saver.save(sess, './data/saved.ckpt')
        print("학습된 모델 저장 완료 !!")
