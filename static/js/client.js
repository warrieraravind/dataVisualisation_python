queue()
    .defer(d3.json, "/setup")
    .await(render_scatter);

funcObj = {
    'scatter_tab':
        render_scatter,
    'scree_tab':
        render_scree,
    'intrinsic_tab':
        render_intrinsic_plot
}
function setTab(val){
    setTabInactive()
    document.getElementById(val).classList.add("active")

    queue()
        .defer(d3.json, "/" + val)
        .await(funcObj[val]);
}



function render_scree(error, result_json){
    d3.selectAll('svg').remove()

    random = result_json['random']
    stratified = result_json['stratified']

    render_bar('random_sampling_scatter_plot', (random['random_pca_sum_squared']))
    render_bar('stratified_sampling_scatter_plot', (stratified['stratified_pca_sum_squared']))

}

function objectToArray(obj){
    returnArr = [];
    for (attr in obj){
        returnArr.push([attr, obj[attr]])
    }

    return returnArr;
}

function setTabInactive(){
    ids = ["scatter_tab", "scree_tab", "intrinsic_tab"]
    for (i = 0; i < ids.length; i++){
        id = ids[i]
        document.getElementById(id).classList.remove("active")
    }
}

function render_bar(id, data){
    var margin = {top: 10, right: 15, bottom: 60, left: 70}
          , width = 400 - margin.left - margin.right
          , height = 300 - margin.top - margin.bottom;

    var svg = d3.select('#' + id)
        .append('svg:svg')
        .attr('width', width + margin.right + margin.left)
        .attr('height', height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    var g = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
    var y = d3.scale.linear().range([height, 0]);

    x.domain(data.map(function(d) { return d[0]; }));
    y.domain([0, d3.max(data, function(d) { return d[1]; })]);



    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10);


    x.domain(data.map(
        function(d) {
            return d[0];
         }));

    y.domain([0, d3.max(data, function(d)
        {
            return d[1];
        })]);


    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .style("text-anchor", "end")
        .style("font-size", "8px")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-25)" );

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("PCA Loadings");

    svg.selectAll("bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d[0]); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d[1]); })
        .attr("height", function(d) { return height - y(d[1]); });
}


function render_scatter(error, result_json){

    if(!error){
        d3.selectAll('svg').remove()
        random = result_json['random']
        stratified = result_json['stratified']

        transformed_random_pc = random['transformed_random_pc']
        transformed_stratified_pc = stratified['transformed_stratified_pc']

        scatter_plot('random_sampling_scatter_plot', transformed_random_pc)
        scatter_plot('stratified_sampling_scatter_plot', transformed_stratified_pc)

}


function scatter_plot(id, data){
    var margin = {top: 20, right: 15, bottom: 60, left: 60}
      , width = 400 - margin.left - margin.right
      , height = 300 - margin.top - margin.bottom;


    random = result_json['random']
    stratified = result_json['stratified']

    var x = d3.scale.linear()
          .domain([d3.min(data, function(d) { return d[0]; }), d3.max(data, function(d) { return d[0]; })])
          .range([ 0, width ]);

    var y = d3.scale.linear()
          .domain([d3.min(data, function(d) { return d[1]; }), d3.max(data, function(d) { return d[1]; })])
          .range([ height, 0 ]);

    var chart = d3.select('#' + id)
        .append('svg:svg')
        .attr('width', width + margin.right + margin.left)
        .attr('height', height + margin.top + margin.bottom)
        .attr('class', 'chart')


    var main = chart.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .attr('width', width)
        .attr('height', height)
        .attr('class', 'main')

    // draw the x axis
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom');

    main.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .attr('class', 'main axis date')
        .call(xAxis)
        .append("text")
        .text("PC 1");

    // draw the y axis
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient('left');

    main.append('g')
        .attr('transform', 'translate(0,0)')
        .attr('class', 'main axis date')
        .call(yAxis)
        .append("text")
        .text("PC 2");

    var g = main.append("svg:g");

    g.selectAll("scatter-dots")
      .data(data)
      .enter().append("svg:circle")
      .attr("cx", function (d,i) { return x(d[0]); } )
      .attr("cy", function (d) { return y(d[1]); } )
      .attr("r", 2);
    }
}