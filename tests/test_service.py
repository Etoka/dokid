import dokid

test_service = dokid.create_service("com.krobix.test0.ini")
test_service1 = dokid.create_service("com.krobix.test0.ini")
test_service.start()
test_service1.start()