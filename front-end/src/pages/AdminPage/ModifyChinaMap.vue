<template>
    <div class="content">
        <!-- 关闭按钮 -->
        <button class="close-button" @click="closeModal">✖</button>
        <div ref="charts" class="chart"></div>
        <!-- 新增的输入字段和按钮 -->
        <div class="form-group">
            <div class="floating-placeholder" :class="floatingPlaceholderClassLongitude">
                <input type="text" id="longitude" v-model="tmpLongitude" placeholder="Longitude"
                    @focus="isLongitudeFocused = true" @blur="isLongitudeFocused = false">
                <label for="longitude">Longitude</label>
            </div>
            <div class="floating-placeholder" :class="floatingPlaceholderClassLatitude">
                <input type="text" id="latitude" v-model="tmpLatitude" placeholder="Latitude"
                    @focus="isLatitudeFocused = true" @blur="isLatitudeFocused = false">
                <label for="latitude">Latitude</label>
            </div>
            <!-- 使用 :disabled 属性来禁用或启用按钮，根据 tmpPoint 是否为 null -->
            <button class="btn btn-primary" @click="confirmLocation" :disabled="!tmpPoint">Confirm</button>
            <button class="btn btn-secondary" @click="resetLocation" :disabled="!tmpPoint">Reset</button>
        </div>
    </div>
</template>

  



  
<script>
import * as echarts from 'echarts'
import china from '@/assets/json/china.json'
export default {

    props: ['longitude', 'latitude', 'dataset_id', 'dataset_name'],
    data() {
        return {
            isLongitudeFocused: false,
            isLatitudeFocused: false,
            tmpPoint: null,
            selectedPoint: {
                longitude: null,
                latitude: null,
                dataset_id: null, // 添加这一行
                dataset_name: null // 添加这一行
            },
            chart: null,
            windTurbineMapping: {},
            points: [],
            tmpLongitude: this.longitude, // 使用从父组件传递的值初始化
            tmpLatitude: this.latitude, // 使用从父组件传递的值初始化
            chartOption: null,
            tmpLocationName: null, // 用于存储选中的地名

        }
    },
    watch: {
        // 监听 tmpLongitude 和 tmpLatitude 的变化
        tmpLongitude(val) {
            this.updateTmpPoint();
        },
        tmpLatitude(val) {
            this.updateTmpPoint();
        },
    },

    computed: {
        floatingPlaceholderClassLongitude() {
            return this.tmpLongitude ? 'floating-placeholder-float' : '';
        },
        floatingPlaceholderClassLatitude() {
            return this.tmpLatitude ? 'floating-placeholder-float' : '';
        },
    },

    created() {
        console.log("created");
        this.selectedPoint.longitude = this.longitude;
        this.selectedPoint.latitude = this.latitude;
        console.log(this.selectedPoint);
        // 从后端获取风机名称和地名的映射
        this.getWindTurbines();
    },


    beforeDestroy() {
        window.removeEventListener('resize', this.handleResize);
        if (this.chart) {
            this.chart.dispose();
        }
    },
    methods: {
        updateTmpPoint() {
            if (
                this.tmpLongitude !== this.selectedPoint.longitude ||
                this.tmpLatitude !== this.selectedPoint.latitude
            ) {
                this.tmpPoint = {
                    name: 'tmpPoint',
                    value: [this.tmpLongitude, this.tmpLatitude],
                    itemStyle: { color: '#EE66AA' },
                };
            } else {
                this.tmpPoint = null;
            }
            this.updatePoints();
        },

        updatePoints() {
            // 先过滤掉旧的 tmpPoint
            this.points = this.points.filter((point) => point.name !== 'tmpPoint');

            // 更新所有点的样式
            this.points = this.points.map(point => {
                point.itemStyle = this.getItemStyle(point.name);
                return point;
            });

            // 如果 tmpPoint 存在，则添加到 points 中
            if (this.tmpPoint) {
                this.points.push(this.tmpPoint);
            }

            // 仅更新数据，不重新渲染整个图表
            this.chartOption.series[0].data = this.points;
            this.chart.setOption({ series: this.chartOption.series }, false);
        },


        confirmLocation() {
            fetch(`http://127.0.0.1:5000/update_location`, {
                method: 'post',
                body: JSON.stringify({
                    'dataset_id': this.dataset_id, // 使用从 props 传递的 dataset_id
                    'location': this.tmpLocationName,
                    'longitude': this.tmpLongitude,
                    'latitude': this.tmpLatitude
                }),
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.hasOwnProperty('error')) {
                        this.$message({
                            message: data['error'],
                            type: 'warning'
                        })
                        return
                    }
                    // 更新选中的点和临时点
                    this.selectedPoint.longitude = this.tmpLongitude;
                    this.selectedPoint.latitude = this.tmpLatitude;
                    this.tmpPoint = null;


                    // 更新地图上的点的映射
                    const key = this.dataset_name; // 使用从 props 传递的 dataset_name
                    console.log(key);
                    this.windTurbineMapping[key] = [this.tmpLongitude, this.tmpLatitude];
                    console.log(this.windTurbineMapping);

                    // 更新地图上的点
                    this.points = this.points.map(point => {
                        if (point.name === key) {
                            point.value = [this.tmpLongitude, this.tmpLatitude];
                        }
                        return point;
                    });


                    // 更新地图上的点的样式
                    this.updatePoints();


                    // 更新父组件的经纬度
                    this.$emit('update-location', {
                        longitude: this.tmpLongitude,
                        latitude: this.tmpLatitude,
                        location: this.tmpLocationName,
                        dataset_id: this.dataset_id,
                        dataset_name: this.dataset_name
                    });


                    this.$message({
                        message: data['result'],
                        type: 'success'
                    })

                })
        },



        resetLocation() {
            // 将 tmpLongitude 和 tmpLatitude 重置为 selectedPoint 的值
            this.tmpLongitude = this.selectedPoint.longitude;
            this.tmpLatitude = this.selectedPoint.latitude;

            // 清空 tmpPoint
            this.tmpPoint = null;

            // 更新点的样式
            this.updatePoints();
        },

        closeModal() {
            // 关闭模态框
            this.$emit('close-map-modal');
        },
        getWindTurbines() {
            fetch(`http://127.0.0.1:5000/get_datasets`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    // 将数据转换为地图组件所需的格式
                    this.points = data.map(item => {
                        return {
                            name: item.dataset_name,
                            value: [item.longitude, item.latitude]
                        };
                    });

                    // 更新风机映射
                    this.windTurbineMapping = data.reduce((mapping, item) => {
                        mapping[item.dataset_name] = { longitude: item.longitude, latitude: item.latitude };
                        return mapping;
                    }, {});


                    // 初始化选中的经纬度
                    this.selectedPoint.longitude = this.longitude;
                    this.selectedPoint.latitude = this.latitude;

                    console.log(this.selectedPoint)

                    this.points = this.points.map(point => {
                        point.itemStyle = this.getItemStyle(point.name);
                        return point;
                    })
                    this.initChartOption()

                    this.initCharts()
                    window.addEventListener('resize', this.handleResize)
                });
        },

        initChartOption() {
            this.chartOption =
            {
                backgroundColor: '#0E2152',// 背景颜色
                geo: {// 地图配置
                    map: 'china',
                    label: { // 图形上的文本标签
                        normal: {// 通常状态下的样式
                            show: true,
                            textStyle: {
                                color: '#fff'
                            }
                        },
                        emphasis: {// 鼠标放上去高亮的样式
                            textStyle: {
                                color: '#fff'
                            }
                        }
                    },
                    itemStyle: {// 地图区域的样式设置
                        normal: { // 通常状态下的样式
                            borderColor: '#5089EC',
                            borderWidth: 1,
                            areaColor: { //地图区域的颜色
                                type: 'radial', // 径向渐变
                                x: 0.5, // 圆心
                                y: 0.5,// 圆心
                                r: 0.8,// 半径
                                colorStops: [
                                    { // 0% 处的颜色
                                        offset: 0,
                                        color: 'rgba(0, 102, 154, 0)'
                                    },
                                    { // 100% 处的颜色
                                        offset: 1,
                                        color: 'rgba(0, 102, 154, .4)'
                                    }
                                ]
                            }
                        },
                        // 鼠标放上去高亮的样式
                        emphasis: {
                            areaColor: '#2386AD',
                            borderWidth: 0
                        }
                    }
                },
                series: [
                    { // 散点系列数据
                        type: 'effectScatter',// 带有涟漪特效动画的散点（气泡）图
                        coordinateSystem: 'geo', //该系列使用的坐标系:地理坐标系
                        // 特效类型,目前只支持涟漪特效'ripple'，意为“涟漪”
                        effectType: 'ripple',
                        // 配置何时显示特效。可选'render'和'emphasis' 。
                        showEffectOn: 'render',
                        rippleEffect: { // 涟漪特效相关配置。
                            period: 10, // 动画的周期，秒数。
                            scale: 4,// 动画中波纹的最大缩放比例。
                            // 波纹的绘制方式，可选 'stroke' 和 'fill'。
                            brushType: 'fill'
                        },
                        zlevel: 1, // 所有图形的 zlevel 值。
                        data: this.points,
                        itemStyle: {
                            emphasis: {
                                borderColor: '#fff',
                                borderWidth: 3
                            }
                        },
                    },
                ]
            }

        },


        getItemStyle(name) {
            const point = this.points.find(point => point.name === name);

            if (this.tmpPoint) {

                if (point && point.value[0] === this.selectedPoint.longitude && point.value[1] === this.selectedPoint.latitude) {
                    return { color: '#808080' }; // 设置为白色并改变大小
                }
            } else {
                if (point && point.value[0] === this.selectedPoint.longitude && point.value[1] === this.selectedPoint.latitude) {
                    console.log("Selected point without tmpPoint:", name);
                    return { color: '#FFAAAA' }; // 保持原颜色并改变大小
                }
            }

            // console.log("Other point:", name);
            return { color: '#00EEFF' }; // 其他点的颜色和大小
        },




        initCharts() {
            this.chart = echarts.init(this.$refs['charts']);
            echarts.registerMap('china', china);
            this.chart.setOption(this.chartOption);
            this.chart.on('click', (e) => {
                // console.log(e);
                const [longitude, latitude] = this.chart.convertFromPixel('geo', [e.event.offsetX, e.event.offsetY]);
                console.log(longitude, latitude);
                this.tmpLongitude = longitude;
                this.tmpLatitude = latitude;
                // 存储选中的地名
                this.tmpLocationName = e.name;
                console.log(this.tmpLocationName);
                this.updateTmpPoint();
            });
        },

        handleResize() {
            if (this.chart) {
                this.chart.resize();
                console.log('resize')
            }
        }
    }
}
</script>


<style scoped>
.floating-placeholder input:focus {
    border-bottom: 1px solid #16d7f0;
    /* 你想要的颜色 */
}


.floating-placeholder {
    position: relative;
    margin-right: 15px;
    width: 30%;
}

.floating-placeholder input {
    font-size: 14pt;
    border: none;
    outline: none;
    width: 100%;
    background: transparent;
    border-bottom: 1px solid #ccc;
    padding: 5px 0;
    color: #ffffff;
    transition: border-color 0.3s ease;
    /* 添加过渡效果 */
}

.floating-placeholder label {
    display: block;
    position: absolute;
    top: 5px;
    left: 0;
    font-size: 14pt;
    transition: transform 160ms ease-out, color 200ms ease-out, top 160ms ease-out;
    transform-origin: 0, 0.0em;
    transform: scale(1, 1) rotateY(0);
    color: #999;
}

.floating-placeholder-float label {
    transform: scale(0.75, 0.75) rotateY(0);
    top: -15px;
    /* 调整上浮的高度 */
    transform-origin: left;
    /* 设置转换的基点为左边 */
    /* left:-5px; 调整左右浮动的位置 */
    color: #9a97e6;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: transparent;
    border: none;
    font-size: 20px;
    cursor: pointer;
    z-index: 111111;
    color: grey;
}

.close-button:hover {
    color: darkgrey;
}

.content {
    background: transparent;
    width: 100%;
    height: 100%;
    position: fixed;
    overflow: auto;
    max-width: 880px;
    max-height: 580px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 4px solid #aec2f1;
    border-radius: 20px;
    box-shadow: 0 0 20px rgb(154, 151, 216);
    background-color: #0E2152;
}

.chart {
    background: transparent;
    width: 100%;
    height: 100%;
    max-width: 880px;
    max-height: 580px;
    position: relative;
    /* 使用相对定位 */
    top: -20px;
    /* 使用负值上移元素，你可以根据需要调整这个值 */

}

.form-group {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 90%;
}

.btn {
    padding: 6px 12px;
}
</style>
