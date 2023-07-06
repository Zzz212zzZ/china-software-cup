<template>
  <div class="card">
    <div class="row">
      <div class="col-lg-7 col-12">
        <div class="card-header" v-if="$slots.header_1 || title_1">
          <slot name="header_1">
            <h4 class="card-title">{{ title_1 }}</h4>
            <p class="card-category" v-if="subTitle_1">{{ subTitle_1 }}</p>
          </slot>
        </div>
        <div class="card-body" v-if="$slots.default">
          <slot></slot>
        </div>
      </div>
      <div class="divider vertical-divider"></div>
      <div class="col-lg-5 col-12">
        <div class="card-header" v-if="$slots.header_2 || title_2">
          <slot name="header_2">
            <h4 class="card-title">{{ title_2 }}</h4>
            <p class="card-category" v-if="subTitle_2">{{ subTitle_2 }}</p>
          </slot>
        </div>
        <div class="card-body" v-if="$slots.body_2">
          <slot name="body_2"></slot>
        </div>
      </div>
    </div>
    <!-- <div class="card-image" v-if="$slots.image">
      <slot name="image"></slot>
    </div>
    <div class="card-header" v-if="$slots.header || title">
      <slot name="header">
        <h4 class="card-title">{{ title }}</h4>
        <p class="card-category" v-if="subTitle">{{ subTitle }}</p>
      </slot>
    </div>
    <div class="card-body" v-if="$slots.default">
      <slot></slot>
    </div>
    <slot name="raw-content"></slot>
    <div class="card-footer" v-if="$slots.footer">
      <hr />
      <slot name="footer"></slot>
    </div> -->
  </div>
</template>
<script>
import { Divider } from 'element-ui'

export default {
  name: "double-card",
  components: {
    Divider
  },

  props: {
    title_1: String,
    subTitle_1: String,
    title_2: String,
    subTitle_2: String,
  },
};
</script>
<style>
.vertical-divider {
  display: inline-block;
  width: 2px;
  height: auto;
  margin: 10px -1px;
  vertical-align: middle;
  position: relative;
}

.divider {
  background-color: #DCDFE6;
  position: relative;
}
</style>