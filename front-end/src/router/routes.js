import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

//Login page
import Login from "@/pages/LoginPage/Login.vue";

import MainDashboard from "@/MainDashboard.vue";

// Client pages
import clientDataAnalysis from "@/pages/ClientPage/dataAnalysis.vue";
import clientDataPreprocess from "@/pages/ClientPage/dataPreprocess.vue";
import clientModelTrain from "@/pages/ClientPage/modelTrain.vue";

// Analyst pages
import analystDataAnalysis from "@/pages/AnalystPage/dataAnalysis.vue";
import analystDataPreprocess from "@/pages/AnalystPage/dataPreprocess.vue";
import analystModelTrain from "@/pages/AnalystPage/modelTrain.vue";

// Admin pages
import adminDataAnalysis from "@/pages/AdminPage/dataAnalysis.vue";
import adminDataPreprocess from "@/pages/AdminPage/dataPreprocess.vue";
import adminModelTrain from "@/pages/AdminPage/modelTrain.vue";


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
                name: "用户数据特征分析",
                component: clientDataAnalysis,
              },
              {
                path: "dataPreprocess",
                name: "用户数据预处理",
                component: clientDataPreprocess,
              },
              {
                path: "modelTrain",
                name: "用户模型训练",
                component: clientModelTrain,
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
                name: "分析员数据特征分析",
                component: analystDataAnalysis,
              },
              {
                path: "dataPreprocess",
                name: "分析员数据预处理",
                component: analystDataPreprocess,
              },
              {
                path: "modelTrain",
                name: "分析员模型训练",
                component: analystModelTrain,
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
                name: "管理员数据特征分析",
                component: adminDataAnalysis,
              },
              {
                path: "dataPreprocess",
                name: "管理员数据预处理",
                component: adminDataPreprocess,
              },
              {
                path: "modelTrain",
                name: "管理员模型训练",
                component: adminModelTrain,
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