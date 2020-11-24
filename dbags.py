import psycopg2

class DBAgs:

    def __init__(self, host, dbname, user, password):
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)

    def get_Contas_Receber(self):
        cur = self.conn.cursor()
        args = (None)
        stmt = """select 
                    e1_cliente,
                    e1_nomcli,
                    sum(e1_saldo) SaldoSaldo,
                    sum(e1_valor) ValorTitulo
                from
                    se1990 s
                where
                    s.d_e_l_e_t_ = ''
                    and s.e1_saldo > 0
                    and to_date(e1_vencto, 'yyyymmdd') <= now()
                group by e1_cliente, e1_nomcli
                order by
                    e1_nomcli """
        cur.execute(stmt,args)
        result = cur.fetchall()
        cur.close()
        return result #[x[0] for x in self.conn.execute(stmt, args)]

    def get_Preço_Item(self, codigo):
        cur = self.conn.cursor()
        stmt =  """select
                        s.b1_xreffab,
                        s.b1_cod,
                        s.b1_desc,
                        da1.da1_prcven,
                        da0.da0_descri,
                        s2.b2_qatu
                    from
                        sb1990 s
                    left outer join da1990 da1 on
                        da1.da1_codpro = s.b1_cod
                        and da1.d_e_l_e_t_ = ''
                    left outer join da0990 da0 on
                        da1.da1_codtab = da0.da0_codtab
                        and da0.d_e_l_e_t_ = ''
                    left outer join sb2990 s2 on
                        s.b1_cod = s2.b2_cod
                        and s2.d_e_l_e_t_ = ''
                    where
                        s.d_e_l_e_t_ = ''
                        and s.b1_xreffab= %s"""
        args = (codigo, )
        cur.execute(stmt, args)
        result = cur.fetchall()
        cur.close()
        return result #[x[0] for x in self.conn.execute(stmt, args)]    