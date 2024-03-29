import { Container, Divider } from "@chakra-ui/react";
import { Route, Routes } from "react-router-dom";
import './App.css';
import { UpdateContactForm } from "./components/ContactForms";
import Contacts from "./components/Contacts";
import NavMenu from "./components/NavMenu";
import Tunnel from "./components/Tunnel";

function App() {
  return (
    <Container>
      <Container textAlign="right" m="10px">
        <NavMenu m="10px" />
        <Divider />
      </Container>

      <Routes>
        <Route path="/tunnel" element={<Tunnel />} />
        <Route path="/contacts" element={<Contacts />} />
        <Route path="/contacts/:id" element={<UpdateContactForm />} />
      </Routes>

    </Container>
  );
}

export default App;
