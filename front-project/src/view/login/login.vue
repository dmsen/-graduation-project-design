<template>
  <div class="login">
    <div class="login2"></div>
    <div class="login-con">
      <Card icon="log-in" title="欢迎访问" :bordered="false">
        <div class="form-con">
          <login-form @on-success-valid="handleSubmit"></login-form>

          <p class="login-tip">输入任意用户名和密码即可</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import LoginForm from "_c/login-form";
import { mapActions } from "vuex";
export default {
  components: {
    LoginForm,
  },
  data() {
    return {};
  },
  methods: {
    ...mapActions(["handleLogin", "getUserInfo"]),
    handleSubmit({ userName, password, optionLevel }) {
      this.handleLogin({ userName, password, optionLevel }).then((res) => {
        console.log(res);
        if (res === "success") {
          const _this = this;
          try {
            _this.getUserInfo();
            _this.$router.push({
              name: this.$config.homeName,
            });
            _this.$Message.success("登陆成功");
          } catch (err) {
            console.log(err);
            _this.$Message.error("登陆失败，请刷新重试");
          }
        } else {
          this.$Message.error(res);
          // 判断登陆次数锁定用户
        }

        // this.getUserInfo().then((res) => {
        //   console.log(res);
        //   console.log(res);
        //   // this.$router.push({
        //   //   name: this.$config.homeName
        //   // });
        // });
      });
    },
  },
};
</script>

<style lang="less">
@import "./login.less";
</style>
