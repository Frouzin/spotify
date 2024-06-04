document.getElementById("previsao-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const dancabilidade = document.getElementById("dancabilidade").value;
    const energia = document.getElementById("energia").value;
    const vivacidade = document.getElementById("vivacidade").value;
    const volume = document.getElementById("volume").value;
    const modo_audio = document.getElementById("modo_audio").value;
    const fala = document.getElementById("fala").value;
    const ritmo = document.getElementById("ritmo").value;
    const assinatura_tempo = document.getElementById("assinatura_tempo").value;
    const valencia_audio = document.getElementById("valencia_audio").value;

    try {
        const res = await fetch('/modo_musica', {
            method: "POST",
            headers: { 
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                dancabilidade: Number(dancabilidade),
                energia: Number(energia),
                vivacidade: Number(vivacidade),
                volume: Number(volume),
                modo_audio: Number(modo_audio),
                fala: Number(fala),
                ritmo: Number(ritmo),
                assinatura_tempo: Number(assinatura_tempo),
                valencia_audio: Number(valencia_audio)
            })
        });

        const data = await res.json();
        const resultado = document.getElementById("resultado");
        if (data.modo_musica !== undefined) {
            resultado.innerText = data.modo_musica === 1 ? "agitado" : "lento";
        } else if (data.erro) {
            resultado.innerText = `Erro: ${data.erro}`;
        } else {
            resultado.innerText = "Erro ao prever o modo de música.";
        }
    } catch (error) {
        console.error("Erro:", error);
        const resultado = document.getElementById("resultado");
        resultado.innerText = "Erro ao prever o modo de música.";
    }
});

am5.ready(function() {
    var root = am5.Root.new("chartsdiv");

    root.setThemes([ am5themes_Animated.new(root) ]);

    var chart = root.container.children.push(am5xy.XYChart.new(root, {
        panX: true,
        panY: true,
        wheelX: "panX",
        wheelY: "zoomX",
        pinchZoomX: true,
    }));

    var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
    cursor.lineY.set("visible", false);

    var xRenderer = am5xy.AxisRendererX.new(root, { 
        minGridDistance: 30, 
        minorGridEnabled: true
    });

    xRenderer.labels.template.setAll({
        rotation: 0,
        centerY: am5.p50,
        centerX: am5.p100,
        paddingRight: -15
    });

    xRenderer.grid.template.setAll({ location: 1 });

    var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
        maxDeviation: 0.3,
        categoryField: "category",
        renderer: xRenderer,
        tooltip: am5.Tooltip.new(root, {})
    }));

    var yRenderer = am5xy.AxisRendererY.new(root, { strokeOpacity: 0.1 });

    var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        maxDeviation: 0.3,
        renderer: yRenderer
    }));

    var series = chart.series.push(am5xy.ColumnSeries.new(root, {
        name: "Series 1",
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: "valor",
        sequencedInterpolation: true,
        categoryXField: "category",
        tooltip: am5.Tooltip.new(root, { labelText: "{valueY}" })
    }));

    series.columns.template.setAll({ cornerRadiusTL: 5, cornerRadiusTR: 5, strokeOpacity: 0 });

    series.columns.template.adapters.add("fill", function (fill, target) {
        return chart.get("colors").getIndex(series.columns.indexOf(target));
    });

    series.columns.template.adapters.add("stroke", function (stroke, target) {
        return chart.get("colors").getIndex(series.columns.indexOf(target));
    });

    fetch('/histograma')
        .then(response => response.json())
        .then(data => {
            xAxis.data.setAll(data);
            series.data.setAll(data);
        });

    series.appear(1000);
    chart.appear(1000, 100);
});


am5.ready(function() {
    var root = am5.Root.new("chartpizza");

    root.setThemes([
        am5themes_Animated.new(root)
    ]);

    fetch('/graficopizza')
        .then(response => response.json())
        .then(data => {
            var chart = root.container.children.push(
                am5percent.PieChart.new(root, {
                    endAngle: 270
                })
            );

            var series = chart.series.push(
                am5percent.PieSeries.new(root, {
                    valueField: "value",
                    categoryField: "category",
                    endAngle: 270
                })
            );

            series.states.create("hidden", {
                endAngle: -90
            });

            series.data.setAll(data);

            series.appear(1000, 100);
        })
        .catch(error => {
            console.error('Erro ao carregar dados do gráfico de pizza:', error);
        });
});