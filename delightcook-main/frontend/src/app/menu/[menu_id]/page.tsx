"use client";

import { ChakraProvider } from "@chakra-ui/react";
import Detail from "@/components/Detail";
import { useRouter, useSearchParams } from 'next/navigation';
import { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import axios from "axios";

export default function MenuDetail(){
   const {menu_id: menu_id_string} = useParams<{menu_id: string}>();
   const menu_id = Number(menu_id_string);
   const router = useRouter();
   const [menuItems, setMenuItems] = useState([]);

   useEffect(() => {
    const fetchData = async () => {
      try {
        const menuItemsResponse = await axios.get(`http://127.0.0.1:8000/menu_items/`);
        setMenuItems(menuItemsResponse.data);
      } catch (error) {
        console.log('error fetching data: ', error);
      }
    };
    fetchData();
  }, []);

   return(
       <ChakraProvider>
           <Detail menu_items={menuItems} status={true} />
       </ChakraProvider>
   )
}
