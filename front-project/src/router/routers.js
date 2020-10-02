import myMain from "@/components/mymain";
import parentView from "@/components/parent-view";
/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  title: { String|Number|Function }
 *         显示在侧边栏、面包屑和标签栏的文字
 *         使用'{{ 多语言字段 }}'形式结合多语言使用，例子看多语言的路由配置;
 *         可以传入一个回调函数，参数是当前路由对象，例子看动态路由和带参路由
 *  hideInBread: (false) 设为true后此级路由将不会出现在面包屑中，示例看QQ群路由配置
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面在切换标签后不会缓存，如果需要缓存，无需设置这个字段，而且需要设置页面组件name属性和路由配置的name一致
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 *  beforeCloseName: (-) 设置该字段，则在关闭当前tab页时会去'@/router/before-close.js'里寻找该字段名对应的方法，作为关闭前的钩子函数
 * }
 */
export default [{
    path: "/login",
    name: "login",
    meta: {
      title: "Login - 登录",
      hideInMenu: true,
    },
    component: () => import("@/view/login/login.vue"),
  },
  {
    path: "/",
    name: "_home",
    redirect: "/home",
    component: myMain,
    meta: {
      hideInMenu: false,
    },
    children: [{
      path: "/home",
      name: "home",
      meta: {
        hideInMenu: false,
        title: "首页",
        icon: "md-home",
      },
      component: () => import("@/view/home/home.vue"),
    }, ],
  },
  {
    path: "/",
    name: "bMap",
    component: myMain,
    meta: {
      hideInMenu: false,
      access: [1, 0, 2],
    },
    children: [{
      path: "/bMap",
      name: "b-map",
      meta: {
        hideInMenu: false,
        title: "百度地图",
        icon: "ios-flower",
      },
      component: () => import("@/view/b-map/b-map.vue"),
    }, ],
  },

  {
    path: "/",
    meta: {
      // hideInMenu: false,
      hideInBread: true,
      access: [1, 0, 2],
    },
    component: myMain,
    children: [{
      path: "/userManagement",
      name: "user-management",
      meta: {
        icon: "ios-flower",
        title: "用户管理",
      },
      component: () => import("@/view/user-management/user-management.vue"),
    }, ],
  },
  {
    path: "/",
    name: "bEcharts",
    meta: {
      icon: "ios-flower",
      title: "百度图表展示",
      showAlways: true,
      access: [1, 0, 2],
    },
    component: myMain,
    children: [{
      path: "/bEcharts",
      name: "b-echarts",
      meta: {
        icon: "ios-flower",
        title: "百度图表1",
      },
      component: () => import("@/view/b-echarts/b-echarts.vue"),
    }, ],
  },
  {
    path: "/",
    name: "websocket",
    meta: {
      icon: "ios-flower",
      title: "实时图表展示",
      showAlways: true,
      access: [1, 0, 2],
    },
    component: myMain,
    children: [{
      path: "/bEcharts",
      name: "dynamic-graph",
      meta: {
        icon: "ios-flower",
        title: "动态图表首页",
      },
      component: () => import("@/view/dynamic-graph/dynamic-graph.vue"),
    }, ],
  },

  {
    path: "/",
    name: "faultProcessing",
    meta: {
      icon: "ios-flower",
      title: "故障（业务）处理流程",
      showAlways: true,
      access: [1, 0, 2],
    },
    component: myMain,
    children: [{
      path: "/faultProcessing",
      name: "fault-processing",
      meta: {
        icon: "ios-flower",
        title: "故障（业务）处理流程1",
      },
      component: () => import("@/view/fault-processing/fault-processing.vue"),
    }, ],
  },
  {
    path: "/",
    name: "Audio",
    meta: {
      hideInMenu: false,
      access: [1, 0, 2],
    },
    component: myMain,
    children: [{
      path: "/audio",
      name: "audio",
      meta: {
        icon: "ios-flower",
        title: "音乐",
      },
      component: () => import("@/view/audio/audio.vue"),
    }, ],
  },
  {
    path: "/",
    name: "Vidio",
    meta: {
      hideInMenu: false,
      access: [1, 0, 2],
    },
    component: myMain,
    children: [{
      path: "/vidio",
      name: "vidio",
      meta: {
        icon: "ios-flower",
        title: "视频",
      },
      component: () => import("@/view/vidio/vidio.vue"),
    }, ],
  },
  {
    path: "/",
    name: "industrialSystem",
    meta: {
      icon: "ios-flower",
      title: "工业数据实时监测系统",
      showAlways: true,
      access: [1, 0, 2],
    },
    component: myMain,
    children: [{
      path: "/bEcharts",
      name: "industrial-system",
      meta: {
        icon: "ios-flower",
        title: "一级导航",
        showAlways: true,
        access: [1, 0, 2],
      },
      component: parentView,
      children: [{
          path: "/bEcharts1",
          name: "industrial-system1",
          meta: {
            icon: "ios-flower",
            title: "二级导航",
          },
          component: () => import("@/view/b-echarts/b-echarts.vue"),
        },
        {
          path: "/bEcharts2",
          name: "industrial-system2",
          meta: {
            icon: "ios-flower",
            title: "二级导航",
          },
          component: () => import("@/view/b-echarts/b-echarts.vue"),
        },
      ],

    }, ],
  },
  {
    path: "/401",
    name: "error_401",
    meta: {
      hideInMenu: true,
    },
    component: () => import("@/view/error-page/401.vue"),
  },
  {
    path: "/500",
    name: "error_500",
    meta: {
      hideInMenu: true,
    },
    component: () => import("@/view/error-page/500.vue"),
  },
  {
    path: "*",
    name: "error_404",
    meta: {
      hideInMenu: true,
    },
    component: () => import("@/view/error-page/404.vue"),
  },
];