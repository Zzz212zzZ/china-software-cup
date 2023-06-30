<template>
    <div class="card">
        <div class="row">
            <!-- 基本描述 -->
            <div class="col-lg-12 col-xl-1">
                <h4 class="card-title">{{title}}</h4>
                <p class="card-category">{{ description }}</p>
            </div>

            <!-- 主体 -->
            <div class="col-lg-12 col-xl-auto card-body">
                <slot></slot>
            </div>

            <!-- 分数 -->
            <!-- <div class="col-lg-12 col-xl-1">
                <slot name="footer"></slot>
            </div> -->

        </div>
    </div>
</template>

<script>
export default {
    name: 'model-card',
    props: {
        title: String,
        description: String,
    }

}
</script>