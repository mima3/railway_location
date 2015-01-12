<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
  <title>路線情報</title>
  <link rel="stylesheet" href="/railway_location/js/select2/select2.css" type="text/css" />
  <link rel="stylesheet" href="/railway_location/js/jquery/jquery-ui.min.css" type="text/css" />
  <link rel="stylesheet" href="/railway_location/base.css" type="text/css" />
  <script type="text/javascript" src="/railway_location/js/jquery/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="/railway_location/js/jquery/jquery-ui-1.10.4.min.js"></script>
  <script type="text/javascript" src="/railway_location/js/select2/select2.min.js"></script>
  <script type="text/javascript" src="/railway_location/js/blockui/jquery.blockUI.js"></script>
  <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
  <script type="text/javascript" src="/railway_location/js/util.js"></script>
  <script type="text/javascript" src="/railway_location/js/railway.js"></script>
</head>
<body>
  <div id="contents">
    運行会社名：<select id="selOperationCompany">
      <option value = ""></option>
      %for c in operation_company:
        <option value = "{{c}}">{{c}}</option>
      %end
    </select>
    路線名：<select id="selRailway"><option>　　　　　　　　　　</option></select>
    <buttion id="showRailway">路線表示</buttion>
    <div id="map_canvas" style="width: 100%; height: 400px"></div>
    <p>このデータは以下から取得したものです</p>
    <p><a href="http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v2_2.html">国土数値情報　鉄道データ</a></p>
  </div>
</body>
</html>
