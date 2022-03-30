import { ArrowForwardIcon, EditIcon, HamburgerIcon } from "@chakra-ui/icons";
import {
  Box,
  IconButton,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
} from "@chakra-ui/react";

const NavMenu = (props) => (
  <Box {...props}>
    <Menu>
      <MenuButton
        as={IconButton}
        aria-label="Options"
        icon={<HamburgerIcon />}
        variant="outline"
      />
      <MenuList>
        <MenuItem as="a" href="/tunnel" icon={<ArrowForwardIcon />}>
          Tunnel
        </MenuItem>
        <MenuItem as="a" href="/contacts" icon={<EditIcon />}>
          Contacts
        </MenuItem>
      </MenuList>
    </Menu>
  </Box>
);

export default NavMenu;
