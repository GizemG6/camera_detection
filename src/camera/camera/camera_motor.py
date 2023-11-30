import rospy2
from std_msgs.msg import String

def talker():
    pub_topic = rospy2.Publisher("konusma", String, queue_size=10)
    rospy2.init_node("talker")

    while not rospy2.is_shutdown():
        rats = rospy2.Rate(2) #2 Hz
        str_hello = String("Hello from talker " + str(rospy2.get_time()))
        rospy2.loginfo(str_hello)
        pub_topic.publish(str_hello)

talker()