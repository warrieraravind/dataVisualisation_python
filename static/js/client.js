queue()
    .defer(d3.json, "/setup")
    .await(render_scatter);

funcObj = {
    'scatter_tab': render_scatter,
    'scree_tab': render_scree,
    'intrinsic_tab': render_intrinsic,
    'elbow_tab': render_elbow,
    'mds_correlation_tab': render_mds_correlation,
    'mds_euclidean_tab': render_mds_euclidean,
    'matrix_random_tab': render_matrix_random,
    'matrix_stratified_tab': render_matrix_stratified

}

function render_scree(error, result_json) {
    displayOn('split_col')
    displayOff('single_col')
    d3.selectAll('svg').remove()

    random = result_json['random']
    stratified = result_json['stratified']

    render_bar('random_sampling_scatter_plot', (random['random_pca_sum_squared']))
    render_bar('stratified_sampling_scatter_plot', (stratified['stratified_pca_sum_squared']))

}

function render_intrinsic(error, result_json) {
    if (!error) {
        displayOn('split_col')
        displayOff('single_col')
        d3.selectAll('svg').remove()
        random = result_json['random']
        stratified = result_json['stratified']

        render_line_plot('random_sampling_scatter_plot', convert1Dto2D(random['eigen_value_random']), 400, 300, 0, 'Index', 'Eigen Value')
        render_line_plot('stratified_sampling_scatter_plot', convert1Dto2D(stratified['eigen_value_stratified']), 400, 300, 0, 'Index', 'Eigen Value')
    }
}

function render_elbow(error, result_json) {
    if (!error) {
        displayOff('split_col')
        displayOn('single_col')
        d3.selectAll('svg').remove()

        document.getElementById('single_col_title').innerHTML = 'K Means Elbow'

        data = result_json['elbow']
        render_line_plot('elbow_svg', convert1Dto2D(data), 600, 450, 30, '# of Cluster', 'Error')
    }
}

function render_mds_correlation(error, result_json) {
    if (!error) {
        displayOn('split_col')
        displayOff('single_col')
        d3.selectAll('svg').remove()
        displayOn('split_col')
        displayOff('single_col')

        random = result_json['random']
        stratified = result_json['stratified']

        scatter_plot('random_sampling_scatter_plot', random['mds_random_correlation'])
        scatter_plot('stratified_sampling_scatter_plot', stratified['mds_stratified_correlation'])
    }
}

function render_mds_euclidean(error, result_json) {
    if (!error) {
        displayOn('split_col')
        displayOff('single_col')
        d3.selectAll('svg').remove()
        displayOn('split_col')
        displayOff('single_col')

        random = result_json['random']
        stratified = result_json['stratified']

        scatter_plot('random_sampling_scatter_plot', random['mds_random_euclidean'])
        scatter_plot('stratified_sampling_scatter_plot', stratified['mds_stratified_euclidean'])
    }
}

function render_scatter(error, result_json) {

    if (!error) {

        displayOn('split_col')
        displayOff('single_col')

        d3.selectAll('svg').remove()
        random = result_json['random']
        stratified = result_json['stratified']

        transformed_random_pc = random['transformed_random_pc']
        transformed_stratified_pc = stratified['transformed_stratified_pc']

        scatter_plot('random_sampling_scatter_plot', transformed_random_pc)
        scatter_plot('stratified_sampling_scatter_plot', transformed_stratified_pc)
    }
}

function render_matrix_random(error, result_json) {
    if (!error) {
        displayOn('single_col')
        displayOff('split_col')
        d3.selectAll('svg').remove()

        document.getElementById('single_col_title').innerHTML = 'Matrix Scatter Plot - Random'

        indices = result_json["indices"]
        data = result_json['normalized_random_sample']
        labels = result_json['labels']

        newData = extractFields(data, indices)


        render_matrix('elbow_svg', newData, [0, 1, 2], labels)
    }
}

function render_matrix_stratified(error, result_json) {
    if (!error) {
        displayOn('single_col')
        displayOff('split_col')
        d3.selectAll('svg').remove()

        document.getElementById('single_col_title').innerHTML = 'Matrix Scatter Plot - Stratified'

        indices = result_json["indices"]
        data = result_json['normalized_stratified_sample']
        labels = result_json['labels']
        newData = extractFields(data, indices)

        render_matrix('elbow_svg', newData, [0,1,2], labels)
    }
}


function scatter_plot(id, data) {
    var margin = {
            top: 20,
            right: 15,
            bottom: 60,
            left: 60
        },
        width = 400 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain([d3.min(data, function(d) {
            return d[0];
        }), d3.max(data, function(d) {
            return d[0];
        })])
        .range([0, width]);

    var y = d3.scale.linear()
        .domain([d3.min(data, function(d) {
            return d[1];
        }), d3.max(data, function(d) {
            return d[1];
        })])
        .range([height, 0]);

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
        .attr("cx", function(d, i) {
            return x(d[0]);
        })
        .attr("cy", function(d) {
            return y(d[1]);
        })
        .attr("r", 2);
}

function render_bar(id, data) {
    var margin = {
            top: 10,
            right: 15,
            bottom: 60,
            left: 70
        },
        width = 400 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

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

    x.domain(data.map(function(d) {
        return d[0];
    }));
    y.domain([0, d3.max(data, function(d) {
        return d[1];
    })]);



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

    y.domain([0, d3.max(data, function(d) {
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
        .attr("transform", "rotate(-25)");

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("y", 3)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("MSE")
        .attr("transform", "translate(-20,5)")



    svg.selectAll("bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) {
            return x(d[0]);
        })
        .attr("width", x.rangeBand())
        .attr("y", function(d) {
            return y(d[1]);
        })
        .attr("height", function(d) {
            return height - y(d[1]);
        });
}

function render_line_plot(id, data, w, h, translate_x, x_axis_text, y_axis_text) {

    var margin = {
            top: 10,
            right: 15,
            bottom: 60,
            left: 70
        },
        width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var x = d3.scale.linear().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    var valueline = d3.svg.line()
        .x(function(d) {
            return x(d[0]);
        })
        .y(function(d) {
            return y(d[1]);
        });

    var svg = d3.select('#' + id)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + (margin.left + translate_x) + "," + margin.top + ")");

    // Scale the range of the data

    x.domain(d3.extent(data, function(d) {
        return d[0];
    }));
    y.domain([0, d3.max(data, function(d) {
        return d[1];
    })]);

    var lineData = [{
        "x": 0,
        "y": y(1)
    }, {
        "x": width,
        "y": y(1)
    }]

    var func = d3.svg.line()
        .x(function(d) {
            return d.x;
        })
        .y(function(d) {
            return d.y;
        })
        .interpolate("linear")

    var lineGraph = svg.append('path')
        .attr("d", func(lineData))
        .attr("stroke", "black")
        .attr("stroke-width", 2)
        .attr("fill", "none")

    // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .append("text")
        .text(x_axis_text)
        .attr("transform", "translate(290, 20)")


    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .text(y_axis_text)


}

function render_matrix(id, data, indices, labels) {

    var width = 1060,
        size = 230,
        padding = 20;

    var x = d3.scale.linear()
        .range([padding / 2, size - padding / 2]);

    var y = d3.scale.linear()
        .range([size - padding / 2, padding / 2]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(6);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(6);

    var color = d3.scale.category10();

    var traits = indices,
    n = traits.length,
    domainByTrait = {}

    traits.forEach(function(trait) {
        domainByTrait[trait] = d3.extent(data, function(d) { return d[trait]; });
    });

    xAxis.tickSize(size * n);
    yAxis.tickSize(-size * n);

    var svg = d3.select('#' + id).append("svg")
        .attr("width", size * n + padding)
        .attr("height", size * n + padding)
        .append("g")
        .attr("transform", "translate(" + padding + "," + padding / 2 + ")");

    svg.selectAll(".x.axis")
        .data(traits)
        .enter().append("g")
        .attr("class", "x axis")
        .attr("transform", function(d, i) {
            return "translate(" + (n - i - 1) * size + ",0)";
        })
        .each(function(d) {
            x.domain(domainByTrait[d]);
            d3.select(this).call(xAxis);
        });

    svg.selectAll(".y.axis")
        .data(traits)
        .enter().append("g")
        .attr("class", "y axis")
        .attr("transform", function(d, i) {
            return "translate(0," + i * size + ")";
        })
        .each(function(d) {
            y.domain(domainByTrait[d]);
            d3.select(this).call(yAxis);
        });

    var cell = svg.selectAll(".cell")
        .data(cross(traits, traits))
        .enter().append("g")
        .attr("class", "cell")
        .attr("transform", function(d) {
            return "translate(" + (n - d.i - 1) * size + "," + d.j * size + ")";
        })
        .each(plot);

    // Titles for the diagonal.
    cell.filter(function(d) {
            return d.i === d.j;
        }).append("text")
        .attr("x", padding)
        .attr("y", padding)
        .attr("dy", ".71em")
        .text(function(d) {
            return labels[d.x];
        });

    function plot(p) {
        var cell = d3.select(this);

        x.domain(domainByTrait[p.x]);
        y.domain(domainByTrait[p.y]);

        cell.append("rect")
            .attr("class", "frame")
            .attr("x", padding / 2)
            .attr("y", padding / 2)
            .attr("width", size - padding)
            .attr("height", size - padding);

        cell.selectAll("circle")
            .data(data)
            .enter().append("circle")
            .attr("cx", function(d) {
                return x(d[p.x]);
            })
            .attr("cy", function(d) {
                return y(d[p.y]);
            })
            .attr("r", 4)
            .style("fill", function(d) {
                return color(p.x);
            });

    }

    function cross(a, b) {
        var c = [],
            n = a.length,
            m = b.length,
            i, j;
        for (i = -1; ++i < n;)
            for (j = -1; ++j < m;) c.push({
                x: a[i],
                i: i,
                y: b[j],
                j: j
            });
        return c;
    }
}

function extractFields(data, indices) {
    returnArr = []

    for (var i = 0; i < data.length; i++) {
        datum = data[i]
        arr = []
        for (var index = 0; index < indices.length; index++)
            arr.push(datum[indices[index]])
        returnArr.push(arr)
    }


    return returnArr
}

function setTab(val) {
    setTabInactive()
    document.getElementById(val).classList.add("active")

    queue()
        .defer(d3.json, "/" + val)
        .await(funcObj[val]);
}

function convert1Dto2D(arr) {
    returnArr = []
    for (var i = 0; i < arr.length; i++)
        returnArr.push([i, arr[i]])
    return returnArr
}

function displayOn(id) {
    document.getElementById(id).style.display = 'block'
}

function displayOff(id) {
    document.getElementById(id).style.display = 'none'
}

function objectToArray(obj) {
    returnArr = [];
    for (attr in obj) {
        returnArr.push([attr, obj[attr]])
    }

    return returnArr;
}

function setTabInactive() {
    ids = ["scatter_tab", "scree_tab", "intrinsic_tab", "elbow_tab", "mds_correlation_tab", "mds_euclidean_tab", "matrix_random_tab", "matrix_stratified_tab"]
    for (i = 0; i < ids.length; i++) {
        id = ids[i]
        document.getElementById(id).classList.remove("active")
    }
}


function reset() {
    queue()
        .defer(d3.json, "/setup")
        .await(new_data);
}

function new_data(error, result_json) {
    if (!error) {
        render_scatter(error, result_json)
        setTabInactive()
        setTab('scatter_tab')
    }
}