import cv2
import numpy as np
# 全局变量，用于记录鼠标点击的点的坐标
def sharpen_image(image):
    # 创建锐化滤波器的卷积核
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    # 对图像应用卷积操作
    image = cv2.filter2D(image, -1, kernel)
    return image
def DetectImageProgress(image,LX,LY):
    #image=cv2.imread('tutu4.png')
    image = cv2.blur(image, (5, 5))
    image = sharpen_image(image)
    hsv_image=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 定义红的HSV范围
    lower_red=np.array([160, 100, 100])
    upper_red=np.array([180, 255, 255])
    # 定义绿色的HSV范围
    lower_green=np.array([75, 80, 80])
    upper_green=np.array([90, 255, 255])
    # 定义黄色的HSV范围
    lower_yellow=np.array([20, 80, 80])
    upper_yellow=np.array([30, 255, 255])
    # 创建遮罩
    r_m=cv2.inRange(hsv_image, lower_red, upper_red)
    y_m=cv2.inRange(hsv_image, lower_green, upper_green)
    b_m=cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    # 寻找红色区域的中心点
    contours, _=cv2.findContours(r_m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # 寻找最大的红色区域
        max_contour=max(contours, key=cv2.contourArea)
        # 计算最大红色区域的中心点
        M=cv2.moments(max_contour)
        RC=(int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])) if M["m00"] != 0 else [0,0]
    else:
        RC=[0,0]
    # 执行Shi-Tomasi角点检测
    def detect_corners(mask):
        corners=cv2.goodFeaturesToTrack(mask, 10000, 0.01, 5)
        corners=np.int0(corners)if corners is not None else []
        return corners
    # 在绿色区域找到角点
    y_cnrs=detect_corners(y_m)
    # 在黄色区域找到角点
    b_cnrs=detect_corners(b_m)
    if type(y_cnrs)==list or type(b_cnrs)==list or len(y_cnrs)<2 or len(b_cnrs)<2:
        return "未找到角点"
    Yline_=0
    # 标记绿色矩形的角点
    for point1 in y_cnrs:
        x1, y1=point1.ravel()
        for point2 in y_cnrs:
            x2, y2=point2.ravel()
            if x1!=x2:
                newLine_=np.sqrt((x2-x1)**2+(y2-y1)**2)
                if newLine_>Yline_:
                    Yline_=newLine_
                    YLD_=([x1,y1],[x2,y2])
    cv2.line(image, YLD_[0], YLD_[1], (0, 255, 0), 2)
    # 标记黄色矩形的角点
    Bline_=0
    for point1 in b_cnrs:
        x1, y1=point1.ravel()
        for point2 in b_cnrs:
            x2, y2=point2.ravel()
            if x1!=x2:
                newLine_=np.sqrt((x2-x1)**2+(y2-y1)**2)
                if newLine_>Bline_:
                    Bline_=newLine_
                    BLD_=([x1,y1],[x2,y2])
    cv2.line(image, BLD_[0], BLD_[1], (0, 255, 0), 2)
    # 计算两条直线的向量
    YLD=np.array([YLD_[1][0]-YLD_[0][0], YLD_[1][1]-YLD_[0][1]]) if np.all(np.abs(np.array(YLD_[0])-np.array(BLD_[0]))<=20) else np.array([YLD_[0][0]-YLD_[1][0], YLD_[0][1]-YLD_[1][1]])
    BLD=np.array([BLD_[1][0]-BLD_[0][0], BLD_[1][1]-BLD_[0][1]]) 
    if np.all(np.abs(np.array(YLD_[0])-np.array(BLD_[0]))>=200):
        YLD=np.array([YLD_[0][0]-YLD_[1][0], YLD_[0][1]-YLD_[1][1]])
        BLD=np.array([BLD_[0][0]-BLD_[1][0], BLD_[0][1]-BLD_[1][1]])
    # 标准化向量
    YLDV=YLD/np.linalg.norm(YLD)
    BLDV=BLD/np.linalg.norm(BLD)
    # 设置移动步长
    step=1
    epsilon=1
    # 在line2上沿着line1的方向移动并扫描
    YCD0=np.array(YLD_[0]).astype(float)
    YCD1=np.array(YLD_[1]).astype(float)
    BCD0=np.array(BLD_[0]).astype(float)
    BCD1=np.array(BLD_[1]).astype(float)
    while True:
        Yx1=int(YCD0[0])
        Yx2=int(YCD1[0])
        Yy1=int(YCD0[1])
        Yy2=int(YCD1[1])
        Bx1=int(BCD0[0])
        Bx2=int(BCD1[0])
        By1=int(BCD0[1])
        By2=int(BCD1[1])
        #cv2.line(image, [int(YCD0[0]),int(YCD0[1])], [int(YCD1[0]),int(YCD1[1])], (0, 255, 0), 2)
        #cv2.line(image, [int(BCD0[0]),int(BCD0[1])], [int(BCD1[0]),int(BCD1[1])], (0, 255, 0), 2)
        YLDD0=np.sqrt((RC[0]-Yx1)**2+(RC[1]-Yy1)**2)
        YLDD1=np.sqrt((RC[0]-Yx2)**2+(RC[1]-Yy2)**2)
        YDL=abs((Yy2-Yy1)*RC[0]-(Yx2-Yx1)*RC[1]+Yx2*Yy1-Yy2*Yx1)/Yline_
        BLDD0=np.sqrt((RC[0]-Bx1)**2+(RC[1]-By1)**2)
        BLDD1=np.sqrt((RC[0]-Bx2)**2+(RC[1]-By2)**2)
        BDL=abs((By2-By1)*RC[0]-(Bx2-Bx1)*RC[1]+Bx2*By1-By2*Bx1)/Bline_
        # 更新当前点
        YCD0+=BLDV*step
        YCD1+=BLDV*step
        BCD0+=YLDV*step
        BCD1+=YLDV*step
        # 检查是否超出line2的范围
        if YDL <= epsilon and abs(YLDD0+YLDD1-Yline_) <= epsilon:
            LY=round((YLDD0/Yline_)*400,2)
        if BDL <= epsilon and abs(BLDD0+BLDD1-Bline_) <= epsilon:
            LX=round((BLDD0/Bline_)*400,2)
        if YCD0[0] < min(BLD_[0][0], BLD_[1][0])-10 or YCD0[0] > max(BLD_[0][0], BLD_[1][0])+10:
            break
    return image,LX,LY
