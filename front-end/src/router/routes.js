import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

//Login page
import Login from "@/pages/LoginPage/Login2.vue";

import MainDashboard from "@/MainDashboard.vue";

// Client pages
import DataAnalysis from "@/pages/ClientPage/dataAnalysis.vue";
import DataPredict from "@/pages/ClientPage/dataPredict.vue";
import UserCenter from "@/pages/ClientPage/UserCenter.vue";

// Analyst pages
import DataPreprocess from "@/pages/AnalystPage/dataPreprocess.vue";
import ModelTrain from "@/pages/AnalystPage/modelTrain.vue";
import ModelManager from "@/pages/AnalystPage/modelManager.vue";

// Admin pages
import UserManager from "@/pages/AdminPage/UserManager.vue";


// const routes = [
//   {
//     path: "/login",
//     component: Login,
//   },
//   {
//     path: "/dashboard",
//     component: DashboardLayout,
    
//         children: [
//           {
//             path: "client/dataAnalysis",
//             name: "用户数据特征分析",
//             component: clientDataAnalysis,
//           },
//           {
//             path: "client/dataPreprocess",
//             name: "用户数据预处理",
//             component: clientDataPreprocess,
//           },
//           {
//             path: "client/modelTrain",
//             name: "用户模型训练",
//             component: clientModelTrain,
//           },
//         ],

//   },
//   { path: "*", component: NotFound },
// ];


const routes = [
  {
    path: "/login",
    component: Login,
  },
  {
    path: "/",
    component: MainDashboard,
    redirect: "/dashboard/client/dataAnalysis",
    children: [
      {
        path: "dashboard",
        component: DashboardLayout,
        children: [
          {
            path: "client",
            redirect: "/dashboard/client/dataAnalysis",
            component: { render: h => h("router-view") },  
            children: [
              {
                path: "dataAnalysis",
                name: "数据特征分析",
                component: DataAnalysis,
              },
              {
                path: "dataPredict",
                name: "数据预测",
                component: DataPredict,
              },
              {
                path: "UserCenter",
                name: "用户中心",
                component: UserCenter,
              },
            ],
          },
          {
            path: "analyst",
            redirect: "/dashboard/analyst/dataAnalysis",
            component: { render: h => h("router-view") },
            children: [
              {
                path: "dataAnalysis",
                name: "数据特征分析",
                component: DataAnalysis,
              },
              {
                path: "dataPreprocess",
                name: "数据预处理",
                component: DataPreprocess,
              },
              {
                path: "modelTrain",
                name: "模型训练",
                component: ModelTrain,
              },
              {
                path: "dataPredict",
                name: "数据预测",
                component: DataPredict,
              },
              {
                path: "ModelManager",
                name: "模型管理",
                component: ModelManager,
              },
              {
                path: "UserCenter",
                name: "用户中心",
                component: UserCenter,
              },
            ],
          },
          {
            path: "admin",
            redirect: "/dashboard/admin/dataAnalysis",
            component: { render: h => h("router-view") },
            children: [
              {
                path: "dataAnalysis",
                name: "数据特征分析",
                component: DataAnalysis,
              },
              {
                path: "ModelManager",
                name: "模型管理",
                component: ModelManager,
              },
              {
                path: "UserManager",
                name: "用户管理",
                component: UserManager,
              },
              {
                path: "UserCenter",
                name: "用户中心",
                component: UserCenter,
              },
            ],
          },
        ],
      },
    ],
  },
  { path: "*", component: NotFound },
];


export default routes;