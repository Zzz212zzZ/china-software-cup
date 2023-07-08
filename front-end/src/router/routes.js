import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

//Login page
import Login from "@/pages/LoginPage/Login.vue";

import MainDashboard from "@/MainDashboard.vue";

// Client pages
import DataAnalysis from "@/pages/ClientPage/dataAnalysis.vue";
import DataPredict from "@/pages/ClientPage/dataPredict.vue";

// Analyst pages
import DataPreprocess from "@/pages/AnalystPage/dataPreprocess.vue";
import ModelTrain from "@/pages/AnalystPage/modelTrain.vue";

// Admin pages
// import adminDataAnalysis from "@/pages/AdminPage/dataAnalysis.vue";
// import adminDataPreprocess from "@/pages/AdminPage/dataPreprocess.vue";
// import adminModelTrain from "@/pages/AdminPage/modelTrain.vue";


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
            ],
          },
        ],
      },
    ],
  },
  { path: "*", component: NotFound },
];


export default routes;