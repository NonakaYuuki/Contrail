import cv2

date_list = []
for i in range(31):
    date_list.append(20220301+i)
for date in date_list:
    for h in ['00','03','06','09','12','15','18','21']:
        path = "/Users/nonakayuuki/Downloads/contrail/[{0}]_{1}h_30000ft.png".format(date,h)
        img = cv2.imread(path)
        height, width = img.shape[:2]


        imageText = img.copy()
        text = '3/{0} {1}h'.format(str(date)[6:],h)
        #始点の座標
        org = (510,450)
        cv2.putText(imageText, text, org, fontFace = cv2.FONT_HERSHEY_TRIPLEX,thickness = 2, fontScale = 1, color = (0,0,0))

        cv2.imshow("Image Text",imageText)
        cv2.imwrite('./result/png/[{0}]_{1}h_30000ft.png'.format(date,h), imageText)