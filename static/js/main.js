CAPTURE_IMG_WIDTH = 640
CAPTURE_IMG_HEIGHT = 480

// Show the selected image to the UI before uploading
function readURL(input, id) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    
    reader.onload = function(e) {
      $(id).attr('src', e.target.result).css({'width': CAPTURE_IMG_WIDTH, 'height': CAPTURE_IMG_HEIGHT});
    }
    
    reader.readAsDataURL(input.files[0]);

    process_upload_another()
  }
}

jQuery.ajaxSetup({
  beforeSend: function() {
     $('#loading').removeClass('hidden');
  },
  complete: function(){
     $('#loading').addClass('hidden');
  },
  success: function() {
    $('#loading').addClass('hidden');
  }
});

// HTML5 WEBCAM
Webcam.set({
  width: CAPTURE_IMG_WIDTH,
  height: CAPTURE_IMG_HEIGHT,
  image_format: 'jpeg',
  jpeg_quality: 90
});
Webcam.attach( '#my-camera' );

let form_capture = document.getElementById('form-capture-image')
$('.btn-capture-image').on('click', function(e) {
  e.preventDefault();

  Webcam.snap(function(data_uri) {
    // display results in page
    readURL(data_uri, '#input-data-uri')

    $('#results').removeClass('hidden')
    $('#taken-photo').attr('src', data_uri)
  });
});

$('#predict-now').on('click', function(e) {
  e.preventDefault();

  taken_photo = $('#taken-photo').attr('src')
  let json_data = {'data-uri': taken_photo }

  $.ajax({
    type: 'POST',
    url: '/upload/',
    processData: false,
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    data: JSON.stringify(json_data),
    success: function(data) {
      $('#prediction').text(data['prediction'])
      $('#probs').text(data['probs'])
    }
  });
});

// Handle Predict Correction
$('#form-predict-correction .btn-correction').on('click', function(e) {
  e.preventDefault();

  let label = $(this).attr('data-label')

  handle_predict_correction(label)
})

function handle_predict_correction(label) {
  let correction_form = document.getElementById('form-predict-correction')

  let form_data = new FormData(correction_form);
  form_data.append('correction-label', label)

  $.ajax({
    type: 'POST',
    url: '/predict-correction/',
    processData: false,
    contentType: false,
    data: form_data,
    success: function(data) {
      $('#form-predict-correction .button').addClass('hidden')
      $('#thank-you').text(data['message']);
    }
  });
};