let text_chart_color = "#d47994"
let purple = "#9C27B095"
let pink = "#eb616d95"

// Core Progress Circle
var options_core_cpu = {
  chart: {
    height: 220,
    type: "radialBar"
  },
  plotOptions: {
    radialBar: {
      hollow: {
        background: 'rgba(219, 93, 167, 0.15)',
        size: "60%"
      },
      track: {
        background: '#ffe3e340',
      },
      dataLabels: {
        showOn: "always",
        name: {
          offsetY: -10,
          show: true,
          color: text_chart_color,
          fontSize: "15px"
        },
        value: {
          offsetY: 5,
          color: text_chart_color,
          fontSize: "25px",
          show: true
        }
      }
    }
  },
  fill: {
    type: "gradient",
    gradient: {
      shade: "dark",
      type: "vertical",
      gradientToColors: [pink],
      stops: [0, 100]
    }
  },
  stroke: {
    lineCap: "round",
  },
};
// Gán dữ liệu vào đây
let data = [0, 0, 0, 0]
let label = ["Core 1", "Core 2", "Core 3", "Core 4"]

const core_chart_elements = document.querySelectorAll('#chart-core-cpu');
const core_chart = {}
for (let i = 0; i < core_chart_elements.length; i++) {
  options_core_cpu.series = [data[i]];
  options_core_cpu.labels = [label[i]];
  options_core_cpu.colors = [purple];
  core_chart[label[i]] = new ApexCharts(core_chart_elements[i], options_core_cpu);
  core_chart[label[i]].render();
}


// Progress Circle
var options_total_cpu = {
  chart: {
    height: 280,
    type: "radialBar",
  },
  series: [0],
  colors: [purple],
  plotOptions: {
    radialBar: {
      hollow: {
        // margin: 0,
        size: "60%",
        background: 'rgba(219, 93, 167, 0.15)',
      },
      track: {
        background: '#ffe3e340',
        dropShadow: {
          enabled: true,
          top: 2,
          left: 0,
          blur: 4,
          opacity: 0.15
        }
      },
      dataLabels: {
        name: {
          offsetY: -10,
          color: text_chart_color,
          fontSize: "15px"
        },
        value: {
          color: text_chart_color,
          fontSize: "27px",
          show: true
        }
      }
    }
  },
  fill: {
    type: "gradient",
    gradient: {
      shade: "dark",
      type: "vertical",
      gradientToColors: [pink],
      stops: [0, 100]
    }
  },
  stroke: {
    lineCap: "round"
  },
  labels: ["Total performance"],
  responsive: [{
    breakpoint: 1700,
    options: {
      chart: {
        height: 280,
      },
    }
  },
  {
    breakpoint: 1400,
    options: {
      chart: {
        height: 250,
      },
    }
  },
  {
    breakpoint: 1281,
    options: {
      chart: {
        height: 280,
      },
    }
  }
],
};
const total_cpu_chart = new ApexCharts(document.querySelector("#chart-total-cpu"), options_total_cpu);
total_cpu_chart.render();


// Line chart CPU
var options_linechart = {
  colors: ['#ff764d', '#E91E63'],
  series: [],
  chart: {
    foreColor: '#bc7ec2',
    height: 200,
    width: 530,
    type: 'line',
    zoom: {
      enabled: false
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: [3, 3],
    curve: 'straight',
    dashArray: [0, 0, 0],
    colors: ['#ff764d', '#E91E63'],
  },
  title: {
    text: 'CPU performance & Temperature History',
    align: 'left',
  },
  legend: {
    tooltipHoverFormatter: function (val, opts) {
      return val + ' - ' + opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] + ''
    },
  },
  markers: {
    size: 0,
    hover: {
      sizeOffset: 5
    },
    colors: ['#ff764d', '#E91E63'],
  },
  xaxis: {
    color: '#888',
    axisBorder: {
      color: text_chart_color,
    },
    axisTicks: {
      borderType: 'solid',
      color: text_chart_color,
    }
  },
  tooltip: {
    y: [{
        title: {
          formatter: function (val) {
            return val + " (%):"
          }
        }
      },
      {
        title: {
          formatter: function (val) {
            return val + " (deg):"
          }
        }
      },
    ]
  },
  grid: {
    borderColor: text_chart_color,
    strokeDashArray: 2,
  },
  responsive: [{
      breakpoint: 2000,
      options: {
        chart: {
          width: 530,
        },
      }
    },
    {
      breakpoint: 1500,
      options: {
        chart: {
          width: 470,
        },
      }
    },
    {
      breakpoint: 1350,
      options: {
        chart: {
          width: "150%",
        },
      }
    },
    {
      breakpoint: 1281,
      options: {
        chart: {
          width: "220%",
        },
      }
    }
  ],
};
const cpu_chart = new ApexCharts(document.querySelector("#linechart-cpu"), options_linechart);
cpu_chart.render();


// Line chart Network
var options_linechart = {
  colors: ['#ff7070', '#8142ff'],
  series: [],
  chart: {
    foreColor: '#bc7ec2',
    height: 270,
    width: "150%",
    type: 'line',
    zoom: {
      enabled: false
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: [3, 3],
    curve: 'straight',
    dashArray: [0, 0, 0],
    colors: ['#ff7070', '#8142ff'],
  },
  title: {
    text: 'Network Traffic History',
    align: 'left',
  },
  legend: {
    tooltipHoverFormatter: function (val, opts) {
      return val + ' - ' + opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] + ''
    },
  },
  markers: {
    size: 0,
    hover: {
      sizeOffset: 5
    },
    colors: ['#ff7070', '#8142ff'],
  },
  xaxis: {
    color: '#888',
    axisBorder: {
      color: text_chart_color,
    },
    axisTicks: {
      borderType: 'solid',
      color: text_chart_color,
    }
  },
  tooltip: {
    y: [{
        title: {
          formatter: function (val) {
            return val + " (times):"
          }
        }
      },
      {
        title: {
          formatter: function (val) {
            return val + " (times):"
          }
        }
      },
    ]
  },
  grid: {
    borderColor: text_chart_color,
    strokeDashArray: 2,
  },
  responsive: [{
    breakpoint: 2000,
    options: {
      chart: {
        width: 530,
      },
    }
  },
  {
    breakpoint: 1500,
    options: {
      chart: {
        width: 470,
      },
    }
  },
  {
    breakpoint: 1350,
    options: {
      chart: {
        width: "150%",
      },
    }
  },
  {
    breakpoint: 1281,
    options: {
      chart: {
        width: "220%",
      },
    }
  }
],
};
const network_chart = new ApexCharts(document.querySelector("#linechart-network"), options_linechart);
network_chart.render();


// Disk space
var options_disk = {
  chart: {
    height: 180,
    type: "radialBar",
  },

  plotOptions: {
    radialBar: {
      hollow: {
        // margin: 0,
        size: "58%",
        background: 'rgba(219, 93, 167, 0.15)',
      },
      track: {
        background: '#ffe3e340',
        dropShadow: {
          enabled: true,
          top: 2,
          left: 0,
          blur: 4,
          opacity: 0.15
        }
      },
      dataLabels: {
        name: {
          offsetY: -3,
          color: text_chart_color,
          fontSize: "15px"
        },
        value: {
          offsetY: 5,
          color: text_chart_color,
          fontSize: "17px",
          show: true
        }
      }
    }
  },
  fill: {
    type: "gradient",
    gradient: {
      shade: "dark",
      type: "vertical",
      gradientToColors: [pink],
      stops: [0, 100]
    }
  },
  stroke: {
    lineCap: "round"
  },
  labels: ["Progress"],
  responsive: [{
    breakpoint: 1700,
    options: {
      chart: {
        height: 180,
      },
    }
  },
  {
    breakpoint: 1500,
    options: {
      chart: {
        height: 160,
      },
    }
  },
  {
    breakpoint: 1350,
    options: {
      chart: {
        height: 140,
      },
    }
  },
  {
    breakpoint: 1281,
    options: {
      chart: {
        height: 200,
      },
    }
  }
],
};

// Gán dữ liệu vào đây
let data_disk = [0, 0]
let label_disk = ["/", "/boot"]
const charts_disk = {}
const charts_disk_elements = document.querySelectorAll('#chart-diskspace');

for (let i = 0; i < charts_disk_elements.length; i++) {
  options_disk.series = [data_disk[i]];
  options_disk.labels = [label_disk[i]];
  options_disk.colors = [purple];
  charts_disk[label_disk[i]] = new ApexCharts(charts_disk_elements[i], options_disk);
  charts_disk[label_disk[i]].render();
}


// Half Circle for RAM, SWAP
var options_ram_swap = {
  chart: {
    height: 300,
    type: "radialBar",
  },
  series: [67],
  colors: [purple],
  plotOptions: {
    radialBar: {
      hollow: {
        // margin: 0,
        size: "65%",
        background: 'rgba(219, 93, 167, 0.15)',
      },
      track: {
        background: '#ffe3e340',
        dropShadow: {
          enabled: true,
          top: 2,
          left: 0,
          blur: 4,
          opacity: 0.15
        }
      },
      dataLabels: {
        name: {
          offsetY: -10,
          color: text_chart_color,
          fontSize: "13px",
        },
        value: {
          color: text_chart_color,
          fontSize: "27px",
          show: true
        }
      }
    }
  },
  fill: {
    type: "gradient",
    gradient: {
      shade: "dark",
      type: "vertical",
      gradientToColors: [pink],
      stops: [0, 100]
    }
  },
  stroke: {
    lineCap: "round"
  },
};

data_ram_swap = [0, 0]
label_ram_swap = ["RAM performance", "SWAP performance"]

const charts_ram_swap_elements = document.querySelectorAll('#chart-circle');
const memory_chart = {}
for (let i = 0; i < charts_ram_swap_elements.length; i++) {
  options_ram_swap.series = [data_ram_swap[i]];
  options_ram_swap.labels = [label_ram_swap[i]];
  options_ram_swap.colors = [purple];
  memory_chart[label_ram_swap[i]] = new ApexCharts(charts_ram_swap_elements[i], options_ram_swap);
  memory_chart[label_ram_swap[i]].render();
}

/* Service function */
function update_core(core_name, value) {
  if (core_chart[core_name]) {
    core_chart[core_name].updateSeries([value])
  }

}

function update_total_cpu(value) {
  total_cpu_chart.updateSeries([value])
}

function update_temperature(value) {
  if (value) {
    document.querySelector("#temperature").innerText = value.toFixed(2)
  }
}

function update_network(send, receive) {
  document.querySelector("#network-send").innerText = send
  document.querySelector("#network-receive").innerText = receive
}

function update_memory(ram, swap) {
  memory_chart["RAM performance"].updateSeries([ram])
  memory_chart["SWAP performance"].updateSeries([swap])
}

function update_disk(disks) {
  for (let disk in disks) {
    if (charts_disk[disk]) charts_disk[disk].updateSeries([disks[disk].percent])
  }
}