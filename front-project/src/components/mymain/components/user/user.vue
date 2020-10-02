<template>
  <div class="user-avatar-dropdown">
    <Dropdown @on-click="handleClick">
      <Avatar :src="userAvatar" />
      <Icon :size="18" type="md-arrow-dropdown"></Icon>
      <DropdownMenu slot="list">
        <Dropdown placement="right-start">
          <DropdownItem name="changeTheme">更换系统主题</DropdownItem>
          <DropdownMenu slot="list">
            <DropdownItem @click.native="handleChangeTheme('dark')">
              <Icon
                type="md-snow"
                style="color: #666;margin-right: 10px"
                :size="18"
              />dark
            </DropdownItem>
            <DropdownItem @click.native="handleChangeTheme('blue')">
              <Icon
                type="md-snow"
                style="color:blue;margin-right: 10px"
                :size="18"
              />blue
            </DropdownItem>
            <DropdownItem @click.native="handleChangeTheme('light')">
              <Icon
                type="md-snow"
                style="color: #19be6b;margin-right: 10px"
                :size="18"
              />light
            </DropdownItem>
            <DropdownItem @click.native="handleChangeTheme('pink')">
              <Icon
                type="md-snow"
                style="color: #ffa3d5;margin-right: 10px"
                :size="18"
              />pink
            </DropdownItem>
          </DropdownMenu>
        </Dropdown>
        <DropdownItem name="changeInfo" style="margin-top: -20px !important"
          >更改个人信息</DropdownItem
        >
        <DropdownItem name="logout">退出登录</DropdownItem>
      </DropdownMenu>
    </Dropdown>

    <Modal v-model="showModal" title="更改个人信息" width="600px">
      <div>
        <Tabs value="1">
          <TabPane label="基本设置" name="1">
            <div>
              <Form>
                <FormItem label="用户名">
                  <Input v-model="userInfo.userName" />
                </FormItem>
                <FormItem label="密码">
                  <Input v-model="userInfo.password" type="password" />
                </FormItem>
                <FormItem prop="status" label="状态">
                  <Select v-model="userInfo.status" class="formItemInputStyle">
                    <Option :value="0">在校</Option>
                    <Option :value="1">离校</Option>
                  </Select>
                </FormItem>
                <FormItem label="备注">
                  <Input
                    prefix="md-remove"
                    v-model="userInfo.remark"
                    placeholder="备注"
                  />
                </FormItem>
              </Form>
              <p style="text-align: center">
                <Button type="primary" @click="handleSubmit">提交更改</Button>
              </p>
            </div>
          </TabPane>
          <TabPane label="头像" name="2">
            <div class="cropper-example cropper-first">
              <cropper
                :src="exampleImageSrc"
                crop-button-text="确认上传"
                @on-crop="handleCroped"
              ></cropper>
            </div>
          </TabPane>
        </Tabs>
      </div>
      <div slot="footer">
        <span style="margin-right: 12px">请确认账号密码填写完整</span>
      </div>
    </Modal>
  </div>
</template>

<script>
import "./user.less";
import { mapActions } from "vuex";
import Cropper from "@/components/cropper";
export default {
  name: "User",
  components: {
    Cropper,
  },
  props: {
    userAvatar: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      showModal: false,
      exampleImageSrc: "",
      userInfo: {
        userName: "",
        password: "",
        jurisdiction: 2,
        status: 0,
        remark: "",
      },
    };
  },
  methods: {
    ...mapActions(["handleLogOut", "handPersonchange", "UserPicChange"]),
    logout() {
      this.handleLogOut().then(() => {
        this.$router.push({
          name: "login",
        });
      });
    },
    handleClick(name) {
      switch (name) {
        case "logout":
          this.logout();
          break;
        case "changeInfo":
          this.showModal = true;
          break;
      }
    },

    // 修改用户头像
    async handleCroped(blob) {
      const _this = this;
      console.log(blob);
      console.log("修改头像");
      console.log(
        this.$store.state.user.userId,
        this.$store.state.user.userName
      );
      const userId = this.$store.state.user.userId;
      const userName = this.$store.state.user.userName;
      const formData = new FormData();
      formData.append("croppedImg", blob);
      formData.append("userId", userId);
      formData.append("userName", userName);
      const res = await _this.UserPicChange(formData);
      console.log(res);
      if (res.result === 1) {
        _this.$Message.error(res.msg);
      } else {
        _this.$Message.success({
          content: res.msg + "头像修改成功",
          duration: 3,
        });
        this.handleLogOut().then(() => {
          this.$router.push({
            name: "login",
          });
        });
        window.location.reload();
      }
    },
    // 修改用户个人信息
    async handleSubmit() {
      const _this = this;
      const id = _this.$store.state.user.userId;
      try {
        const name = this.userInfo.userName;
        const password = this.userInfo.password;
        const status = this.userInfo.status;
        const remark = this.userInfo.remark;
        const mode = "personInfo";
        const res = await _this.handPersonchange({
          id,
          name,
          password,
          remark,
          status,
          mode,
        });
        console.log(res);
        if (res.result === 1) {
          _this.$Message.error(res.msg);
        } else {
          _this.$Message.success(res.msg);
        }
      } catch (err) {
        console.log(err);
        if (err.response !== undefined) {
          this.$Message.error(err.response.status);
        } else {
          this.$Message.error(err);
        }
      }
      this.handleLogOut().then(() => {
        this.$router.push({
          name: "login",
        });
      });
      window.location.reload();
    },
    handleChangeTheme(theme) {
      localStorage.setItem("themeStyle", theme);
      window.location.reload();
    },
  },
};
</script>
