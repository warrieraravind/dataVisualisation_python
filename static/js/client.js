queue()
    .defer(d3.json, "/setup")
    .await(render);

function render(error, result_json){

    if(!error){
        console.log(result_json)
    }

}