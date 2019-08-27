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
  width: 640,
  height: 480,
  image_format: 'jpeg',
  jpeg_quality: 90
});
Webcam.attach( '#my-camera' );

let form_capture = document.getElementById('form-capture-image')
$('.btn-capture-image').on('click', function(e) {
  e.preventDefault();
  
  amount = $(this).attr('data-amount');

  Webcam.snap(function(data_uri) {
    // display results in page
    readURL(data_uri, '#input-data-uri')

    let formdata_capture = {'amount': amount, 'data-uri': data_uri }

    $.ajax({
      type: 'POST',
      url: '/upload-image/',
      processData: false,
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify(formdata_capture),
      success: function(data) {
        $('#results').text('')
        $('#results').append("<h3 class=\"title text-grads-3\">Image saved</h3><img src=\"" + data_uri + "\" alt='' width='" + CAPTURE_IMG_WIDTH/2 + "' height='" + CAPTURE_IMG_HEIGHT/2 + "'/>")
      }
    });
  });
})

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