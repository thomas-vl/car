import tensorflow as tf

X = tf.placeholder(tf.float32, [None, 640, 480, 3])
W = tf.Variable(tf.zeros([921600,4]))
b = tf.Variable(tf.zeros([4]))
#init = tf.initialize_all_variables()
init = tf.global_variables_initializer()

#model
Y=tf.nn.softmax(tf.matmul(tf.reshape(X,[-1,921600]), W) + b)

#placeholder for correct answers
Y_ = tf.placeholder(tf.float32, [None, 4])

#loss fucntion
cross_entropy = -tf.reduce_sum(Y_ * tf.log(Y))

# % of correct answoers in
is_correct = tf.equal(tf.argmax(Y,1),tf.argmax(Y_,1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

optimizer = tf.train.GradientDescentOptimizer(0.003)
train_step = optimizer.minimize(cross_entropy)

sess = tf.Session()
sess.run(init)

for i in range(1):
    print("test")
    #Load correct answers?
    batch_X, batch_Y = ??
    train_data={X: batch_X, Y_: batch_Y}

    sess.run(train_step, feed_dict=train_data)

    a,c = sess.run([accuracy, cross_entropy], feed=train_data)

    test_data={X:}
