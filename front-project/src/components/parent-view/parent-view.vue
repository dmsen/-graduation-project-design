<template>
  <Layout style="height: 100%" class="main">
    <Content class="content-wrapper">
      <keep-alive>
        <router-view />
      </keep-alive>
      <ABackTop
        :height="100"
        :bottom="80"
        :right="50"
        container=".content-wrapper"
      ></ABackTop>
    </Content>
  </Layout>
</template>
<script>
import ABackTop from "_c/mymain/components/a-back-top";
export default {
  name: "ParentView",
  components: {
    ABackTop
  },
  computed: {}
};
</script>
