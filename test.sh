# test face++api
curl -X POST "https://api-cn.faceplusplus.com/imagepp/v1/mergeface" \
-F "api_key=toVgoowXQnV06nZWF_J1WdZRxWZ0ZYFn"  \
-F "api_secret=1O-O5KTElvE5NPGBPQnmZvFtqIgMlSxU"  \
-F "template_file=@model.jpg" \
-F "template_rectangle=70,80,100,100" \
-F "merge_file=@test.jpg" \
-F "merge_rate=70"
