const ipconfig = "140.121.199.231:27018";

function init()
{
    $.ajax({
        url:'http://'+ipconfig+'/api/allCompany',
        dataType: 'json',
        success: function(data) {
          for(let i=0;i<data.length;i++)
          {
            
            console.log(data[i]['companyDetail']);
            console.log(data[i]['companyName']);
          }
        }
      });
}


window.addEventListener("load", init, false);