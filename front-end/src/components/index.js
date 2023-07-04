import FormGroupInput from "./Inputs/formGroupInput.vue";

import DropDown from "./Dropdown.vue";
import PaperTable from "./PaperTable.vue";
import Button from "./Button";

import Card from "./Cards/Card.vue";
import ChartCard from "./Cards/ChartCard.vue";
import StatsCard from "./Cards/StatsCard.vue";
import EchartsCard from "./Cards/EchartsCard.vue";
import DecoratedEchart from "./Cards/DecoratedEchart.vue";
import ModelCard from "./Cards/ModelCard.vue"

import SidebarPlugin from "./SidebarPlugin/index";

import Modal from "./Modals/Modal.vue";

let components = {
  FormGroupInput,
  Card,
  ChartCard,
  StatsCard,
  PaperTable,
  DropDown,
  SidebarPlugin,
  EchartsCard,
  DecoratedEchart,
  ModelCard,
  Modal,
};

export default components;

export {
  FormGroupInput,
  Card,
  ChartCard,
  StatsCard,
  PaperTable,
  DropDown,
  Button,
  EchartsCard,
  DecoratedEchart,
  ModelCard,
  Modal,
};
