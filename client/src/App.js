import { Container, Divider } from "@chakra-ui/react";
import { Route, Routes, useLocation } from "react-router-dom";
import './App.css';
import { UpdateContactForm } from "./components/ContactForms";
import Contacts from "./components/Contacts";
import NavMenu from "./components/NavMenu";

function App() {
  return (
    <Container>
      <Container textAlign="right" m="10px">
        <NavMenu m="10px" />
        <Divider />
      </Container>

      <Routes>
        <Route path="/" element={<PlaceHolderComponent />} />
        <Route path="/tunnel" element={<PlaceHolderComponent />} />
        <Route path="/contacts" element={<Contacts />} />
        <Route path="/contacts/:id" element={<UpdateContactForm />} />
      </Routes>

    </Container>
  );
}

export default App;


const PlaceHolderComponent = () => {
  const location = useLocation();
  return (
    <div>
      <h1>PlaceHolderComponent, current url: {location.pathname}</h1>
    </div>
  );
}

