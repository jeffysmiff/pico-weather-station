$('#date').textfill({maxFontPixels: 1000});
$('#time').textfill({maxFontPixels: 1000});
$('#temperature').textfill({maxFontPixels: 1000});
$('#windspeed').textfill({maxFontPixels: 1000});
$('#pressure').textfill({maxFontPixels: 1000});
$('#humidityvalue').css("font-size", $("#pressurevalue").css("font-size"));
$( document ).ready(function() {
    getData();
});
function getData() {
    console.log('Getting data');
    $.ajax({
        type: 'GET',
        url: 'http://192.168.0.28',
        dataType: 'json'

    })
    .done(function(data) {
            console.log('Success');
            console.log(JSON.stringify(data,null,2));
            var dateFromJson = data.time;
            var currentTime = moment(dateFromJson, 'YYYY/MM/DD-HH-mm-ss');
            $('#datevalue').text(currentTime.format('MMMM Do YYYY'));
            $('#timevalue').text(currentTime.format('HH:mm'));
            $('.flex-container').css('background', data.tempcolour);
            $('#tempvalue').html(Math.round(data.temperature) + '&#176;C');
            $('#pressurevalue').text('Pressure: ' + data.pressure + 'hPa');
            $('#humidityvalue').text('Humidity: ' + data.humidity + '%');
            $('#windvalue').text('Wind: ' + (Math.round(data.wind_speed * 100) / 100).toFixed(2) + 'mph');
            $('#date').textfill({maxFontPixels: 1000, changeLineHeight: true});
            $('#windvalue').css('font-size', $('#datevalue').css('font-size'));
            $('#timevalue').css('font-size', $('#datevalue').css('font-size'));
            $('#temperature').textfill({maxFontPixels: 1000});
            var datetextsize = parseInt($('#datevalue').css('font-size'));
            console.log('Large text size = ' + datetextsize);
            var smalltextsize = Math.round(( datetextsize * 0.75));
            console.log('Small text size = ' + smalltextsize);
            $('#pressurevalue').css('font-size', $('#datevalue').css('font-size') * 0.75);
            $('#humidityvalue').css('font-size', $('#datevalue').css('font-size') * 0.75);
        })
    .fail(function(jqXHR, textStatu) {
        console.log('Failure: ' + textStatus);
        $('#tempvalue').text('Unable to retrieve temperature');
        $('#temperature').textfill({maxFontPixels: 1000});
    })
    .always(function() {
        console.log('Scheduling next update');
        setTimeout(getData, 5000);
    })
}