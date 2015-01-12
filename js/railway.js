$(function() {
  $(document).ready(function() {
    var pt = new google.maps.LatLng(41.925926, 143.240137);
    var mapOptions = {
      center: pt,
      zoom: 7
    };
    var map = new google.maps.Map(
      document.getElementById('map_canvas'),
      mapOptions
    );
    $('#selOperationCompany').select2({
      width: 'resolve' ,
      dropdownAutoWidth: true
    });
    $('#selOperationCompany').change(function() {
      var operationCompany = $('#selOperationCompany').val();
      if (!operationCompany) {
        return;
      }
      $('#selRailway').select2('val', '');
      $('#selRailway').empty();
      util.getJson(
        '/railway_location/json/get_railway_line',
        {
          operation_company: operationCompany
        },
        function (errCode, result) {
          if (errCode) {
            return;
          }
          var opt = $('<option>').html('').val('');
          $('#selRailway').append(opt);
          for (var i = 0; i < result.length; ++i) {
            var opt = $('<option>').html(result[i]).val(result[i]);
            $('#selRailway').append(opt);
          }
        },
        function() {
          $.blockUI({ message: '<img src="/railway_location/img/loading.gif" />' });
        },
        function() {
          $.unblockUI();
        }
      );
    }).keyup(function() {
      $(this).blur().focus();
    });

    $('#selRailway').select2({
      width: 'resolve' ,
      dropdownAutoWidth: true
    });

    var railwayLines=[];
    var stationLines=[];
    var stationInfo=[];
    $('#showRailway').button().click(function() {
      var railway = $('#selRailway').val();
      var operationCompany = $('#selOperationCompany').val();

      console.log(railway);
      if (!railway) {
        return;
      }
      if (!operationCompany) {
        return;
      }
      util.getJson(
        '/railway_location/json/get_railway_curve',
        {
          railway: railway,
          operation_company: operationCompany
        },
        function (errCode, result) {
          console.log(errCode);
          console.log(result);
          if (errCode) {
            return;
          }
          for(var i = 0; i < railwayLines.length; ++i) {
            railwayLines[i].setMap(null);
          }
          railwayLines = [];
          var railroad_curve = result.railroad_curve;
          for (var id in railroad_curve) {
            var points = [];
            for (var i = 0; i < railroad_curve[id].length; ++i) {
              var loc = new google.maps.LatLng(railroad_curve[id][i][0], railroad_curve[id][i][1])
              if (railwayLines.length==0) {
                map.panTo(loc);
              }
              points.push(loc);
            }
            var poly = new google.maps.Polyline({
              path: points,
              strokeColor: "#00FF00",
              strokeOpacity: 1.0,
              strokeWeight: 2
            });
            poly.setMap(map);
            railwayLines.push(poly);
          }        
          // 駅情報
          for(var i = 0; i < stationLines.length; ++i) {
            stationLines[i].setMap(null);
          }
          for(var i = 0; i < stationInfo.length; ++i) {
            stationInfo[i].close();
          }
          stationLines = [];
          stationInfo = [];
          var station = result.station;
          for (var id in station) {
            var points = [];
            var centerPos;
            var ix = Math.ceil(station[id].curve.length / 2) - 1;
            if (station[id].curve.length % 2 != 0) {
                centerPos = new google.maps.LatLng(
                  station[id].curve[ix][0],
                  station[id].curve[ix][1]
                )
            } else {
                centerPos = new google.maps.LatLng(
                  (station[id].curve[ix][0] + station[id].curve[ix+1][0]) / 2,
                  (station[id].curve[ix][1] + station[id].curve[ix+1][1]) / 2
                )
            }
            var infoWnd = new google.maps.InfoWindow({
              content: station[id].name,
              position: centerPos
            });
            infoWnd.open(map);
            stationInfo.push(infoWnd);
            for (var i = 0; i < station[id].curve.length; ++i) {
              var loc = new google.maps.LatLng(
                station[id].curve[i][0],
                station[id].curve[i][1]
              )
              points.push(loc);
            }
            var poly = new google.maps.Polyline({
              path: points,
              strokeColor: "#FF0000",
              strokeOpacity: 1.0,
              strokeWeight: 2
            });
            poly.setMap(map);
            stationLines.push(poly);
          }        
        },
        function() {
          $.blockUI({ message: '<img src="/railway_location/img/loading.gif" />' });
        },
        function() {
          $.unblockUI();
        }
      );
    });
  });
});